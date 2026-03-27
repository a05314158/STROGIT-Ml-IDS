import os, json, redis, traceback, time, ipaddress, threading
import numpy as np
from datetime import datetime, timedelta, timezone

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import func, select
from werkzeug.security import generate_password_hash, check_password_hash
from celery import Celery

# Условный импорт для Postgres (для масштабирования в Docker)
try:
    from sqlalchemy.dialects.postgresql import insert as pg_insert
except ImportError:
    pg_insert = None

from config import app_logger, worker_logger, get_model_user_dir, NUM_FEATURES
from config import DATABASE_URI, SECRET_KEY, ANOMALY_THRESHOLD, TRAINING_SAMPLES_REQUIRED
from extensions import db, login_manager

from models import User, Model, ActiveState, DomainTimeLog, HourlySummary, SensorApiKey
from auth_utils import generate_api_key, hash_api_key, validate_api_key_from_request
from ml_model import TFAutoencoderDetector, IsolationForestDetector
from tasks import train_model_task, predict_anomaly_task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Инициализация Redis & Celery ---
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
celery_app = Celery(app.name, broker=REDIS_URL, backend=REDIS_URL)
r_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


# ==========================================================
# УТИЛИТЫ КАТЕГОРИЗАЦИИ И СЕТИ (Business Logic)
# ==========================================================

def is_internal_ip(ip_str):
    """RFC 1918 Filtering: определяет, является ли узел частью локального контура"""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback
    except:
        return False


def get_cat(dom):
    """Умная классификация трафика для страницы Productivity"""
    d = dom.lower() if dom else ""
    if any(x in d for x in
           ['google', 'stack', 'github', 'slack', 'microsoft', 'jira', 'bitbucket', 'notion']): return 'Work'
    if any(x in d for x in ['youtube', 'twitch', 'netflix', 'vimeo', 'spotify', 'soundcloud']): return 'Entertainment'
    if any(
        x in d for x in ['t.me', 'vk.com', 'facebook', 'instagram', 'x.com', 'linkedin', 'whatsapp']): return 'Social'
    if any(x in d for x in ['binance', 'bybit', 'tradingview', 'crypto']): return 'Finance'
    return 'Systems/Web'


@login_manager.user_loader
def load_user(uid):
    return db.session.get(User, int(uid))


# ==========================================================
# КОРНЕВОЙ API: ПРИЕМ ДАННЫХ (Multi-tenant High Performance)
# ==========================================================

@app.route('/api/sensor_data', methods=['POST'])
def receive_sensor_data():
    """Центральная артерия данных. Принимает векторы от сенсоров разных компаний."""
    try:
        # 1. Быстрая проверка API ключа через кэш в auth_utils
        user = validate_api_key_from_request(request, db.session)
        if not user:
            return jsonify({"status": "unauthorized"}), 401

        data = request.get_json()
        uid = user.id
        status_key = f"status:user:{uid}"
        ts_now = datetime.now(timezone.utc)

        # 2. АТОМАРНОЕ ОБНОВЛЕНИЕ REDIS (Решает гонку состояний)
        # Мы используем pipeline для минимизации задержек сети
        p = r_client.pipeline()
        p.hincrby(status_key, "pkts_total", data.get('packet_count', 0))
        mb_added = round(data.get('total_bytes', 0) / (1024 * 1024), 4)
        p.hincrbyfloat(status_key, "bytes_total_mb", mb_added)
        p.hset(status_key, "active_iface", data.get('interface', 'eth0'))
        p.hset(status_key, "last_ping", str(time.time()))
        p.execute()

        # 3. SQL PERSISTENCE (Bulk Operations)
        # Группируем домены и IP, чтобы не делать 1000 мелких инсертов
        ip_map = data.get('ip_summary', {})
        dom_map = data.get('domain_summary', {})
        hour_key = ts_now.replace(minute=0, second=0, microsecond=0)

        # Обработка Топологии (HourlySummary)
        for ip, vol in ip_map.items():
            # Метод Upsert (для SQLite эмулируем, для Postgres используем ON CONFLICT)
            existing = HourlySummary.query.filter_by(user_id=uid, local_ip=ip, hour_timestamp=hour_key).first()
            if existing:
                existing.total_bytes += vol
                existing.packet_count += data.get('packet_count', 0) // max(len(ip_map), 1)
            else:
                db.session.add(HourlySummary(user_id=uid, local_ip=ip, hour_timestamp=hour_key,
                                             total_bytes=vol,
                                             packet_count=data.get('packet_count', 0) // max(len(ip_map), 1)))

        # Обработка Продуктивности
        for dom, hits in dom_map.items():
            log = DomainTimeLog.query.filter_by(user_id=uid, domain=dom).first()
            if log:
                log.duration_seconds += (hits * 2)  # Эмпирический коэф.
                log.last_seen = ts_now
            else:
                db.session.add(DomainTimeLog(user_id=uid, local_ip=next(iter(ip_map), "0.0.0.0"),
                                             domain=dom, category=get_cat(dom),
                                             duration_seconds=hits * 2, last_seen=ts_now))

        # 4. ML FLOW (Обучение или Детекция)
        m_train = Model.query.filter_by(user_id=uid).filter(Model.progress < 100).first()
        if m_train:
            buffer_key = f"buffer:user:{uid}:model:{m_train.id}"
            r_client.rpush(buffer_key, json.dumps(data['features']))
            curr_size = r_client.llen(buffer_key)

            # Обновляем визуальный прогресс в БД
            progress = int((curr_size / TRAINING_SAMPLES_REQUIRED) * 100)
            m_train.progress = min(progress, 99)
            r_client.hset(status_key, "mode", f"LEARNING ({progress}%)")

            if curr_size >= TRAINING_SAMPLES_REQUIRED:
                samples = [json.loads(x) for x in r_client.lrange(buffer_key, 0, -1)]
                r_client.delete(buffer_key)
                train_model_task.delay(m_train.id, uid, samples)
                r_client.hset(status_key, "mode", "CALIBRATING...")
        else:
            active_m = Model.query.filter_by(user_id=uid, is_active=True).first()
            if active_m:
                r_client.hset(status_key, "mode", "AI ACTIVE")
                predict_anomaly_task.delay(uid, active_m.id, data['features'])

        db.session.commit()
        return jsonify({"status": "ok"}), 202
    except Exception as e:
        db.session.rollback()
        app_logger.error(f"FATAL API ERROR: {traceback.format_exc()}")
        return jsonify({"status": "error", "msg": str(e)}), 500


# ==========================================================
# WEB UI: КЕРНЕЛ РОУТЫ (Полные, как были)
# ==========================================================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/status')
@login_required
def status_poll():
    """Атомарный сбор данных для JS-фронтенда (Dashboards)"""
    uid = current_user.id
    status_hash = r_client.hgetall(f"status:user:{uid}")

    # Собираем логи аномалий
    logs_key = f"logs:user:{uid}"
    logs = r_client.lrange(logs_key, 0, 15)

    return jsonify({
        "mode": status_hash.get("mode", "STANDBY"),
        "pkts_total": int(status_hash.get("pkts_total", 0)),
        "bytes_total_mb": float(status_hash.get("bytes_total_mb", 0.0)),
        "current_score": float(status_hash.get("current_score", 0.0)),
        "active_iface": status_hash.get("active_iface", "WAITING..."),
        "log": logs,
        # Данные моделей для сайдбара
        "models_info": [{"id": m.id, "progress": m.progress, "is_active": m.is_active} for m in current_user.models]
    })


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', models=current_user.models,
                           active_state=current_user.active_state)


@app.route('/productivity')
@login_required
def productivity():
    """Сводка эффективности сети: детализация и распределение по пирогу"""
    details = DomainTimeLog.query.filter_by(user_id=current_user.id) \
        .order_by(DomainTimeLog.duration_seconds.desc()).all()

    stats_query = db.session.query(DomainTimeLog.category, func.sum(DomainTimeLog.duration_seconds)) \
        .filter_by(user_id=current_user.id).group_by(DomainTimeLog.category).all()

    cat_stats = [{"category": r[0], "t": int(r[1])} for r in stats_query]

    formatted_details = []
    for d in details:
        formatted_details.append({'ip': d.local_ip, 'domain': d.domain, 'cat': d.category, 't': d.duration_seconds})

    return render_template('productivity.html', details=formatted_details, cat_stats=cat_stats)


@app.route('/statistics')
@login_required
def statistics():
    """Топология узлов с фильтрацией внутренних адресов"""
    period = request.args.get('period', 'hour')
    delta = timedelta(hours=1) if period == 'hour' else timedelta(days=1)

    q = db.session.query(
        HourlySummary.local_ip,
        func.sum(HourlySummary.total_bytes),
        func.sum(HourlySummary.packet_count)
    ).filter(
        HourlySummary.user_id == current_user.id,
        HourlySummary.hour_timestamp >= datetime.now(timezone.utc) - delta
    ).group_by(HourlySummary.local_ip).all()

    stats = []
    for r in q:
        ip = r[0]
        if is_internal_ip(ip):
            recent = DomainTimeLog.query.filter_by(user_id=current_user.id, local_ip=ip) \
                .order_by(DomainTimeLog.last_seen.desc()).first()
            stats.append({
                'ip': ip,
                'mb': round((r[1] or 0) / (1024 * 1024), 2),
                'packets': r[2],
                'last_seen': recent.last_seen.strftime('%H:%M:%S') if recent else 'STABLE'
            })
    return render_template('statistics.html', stats=stats, period=period)


@app.route('/api_keys')
@login_required
def api_keys():
    return render_template('api_keys.html', api_keys=current_user.api_keys.all())


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


# ==========================================================
# ACTION HANDLERS (Model/Key Lifecycle)
# ==========================================================

@app.route('/create_model', methods=['POST'])
@login_required
def create_model():
    data = request.get_json()
    new_m = Model(name=data['model_name'], model_type=data['model_type'],
                  owner=current_user, progress=0)
    db.session.add(new_m)
    db.session.commit()
    return jsonify({"status": "ok", "model_id": new_m.id})


@app.route('/activate_model', methods=['POST'])
@login_required
def activate_model():
    mid = request.get_json().get('model_id')
    # Деактивируем всё
    Model.query.filter_by(user_id=current_user.id).update({Model.is_active: False})
    m = Model.query.filter_by(id=mid, user_id=current_user.id).first()
    if m:
        m.is_active = True
        st = current_user.active_state or ActiveState(user_id=current_user.id)
        st.is_monitoring, st.active_model_id = True, m.id
        db.session.add(st)
        db.session.commit()
        # Сброс скора в Redis для нового старта
        r_client.hset(f"status:user:{current_user.id}", "current_score", 0.0)
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 404


@app.route('/create_api_key', methods=['POST'])
@login_required
def create_api_key():
    name = request.get_json().get('name', 'Generic Sensor')
    raw_key = generate_api_key()
    new_k = SensorApiKey(user_id=current_user.id, name=name,
                         key_hash=hash_api_key(raw_key), is_active=True)
    db.session.add(new_k)
    db.session.commit()
    return jsonify({"status": "ok", "api_key": raw_key})


@app.route('/delete_api_key', methods=['POST'])
@login_required
def delete_api_key():
    kid = request.get_json().get('key_id')
    k = SensorApiKey.query.filter_by(id=kid, user_id=current_user.id).first()
    if k:
        db.session.delete(k)
        db.session.commit()
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 404


@app.route('/api/stop_training/<int:model_id>', methods=['POST'])
@login_required
def stop_training(model_id):
    m = db.session.get(Model, model_id)
    if m and m.user_id == current_user.id:
        m.progress = 0
        r_client.delete(f"buffer:user:{current_user.id}:model:{model_id}")
        db.session.commit()
        return jsonify({"status": "stopped"})
    return jsonify({"status": "error"}), 404


# ==========================================================
# AUTH FLOW (Standard)
# ==========================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u, e, p = request.form.get('username'), request.form.get('email'), request.form.get('password')
        if User.query.filter_by(email=e).first(): return "Email exists"
        db.session.add(User(username=u, email=e, password_hash=generate_password_hash(p)))
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(email=request.form.get('email')).first()
        if u and check_password_hash(u.password_hash, request.form.get('password')):
            login_user(u)
            return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Запуск сервера на 5000 порту
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)