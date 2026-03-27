from datetime import datetime
from flask_login import UserMixin
from extensions import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    models = db.relationship('Model', backref='owner', lazy='dynamic', cascade="all, delete-orphan")
    time_logs = db.relationship('DomainTimeLog', backref='owner', lazy='dynamic', cascade="all, delete-orphan")
    active_state = db.relationship('ActiveState', backref='owner', uselist=False, cascade="all, delete-orphan")


import os

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    model_path = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    progress = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    __table_args__ = (
        db.Index('idx_user_training', 'user_id', 'progress'),
    )
    
    def delete_files(self):
        """Удаляет файлы модели с диска при удалении записи из БД"""
        if self.model_path:
            try:
                # Удаляем основной файл модели
                if os.path.exists(self.model_path):
                    os.remove(self.model_path)
                
                # Удаляем сопутствующие файлы (scaler, threshold и т.д.)
                base_path = self.model_path.rsplit('.', 1)[0]  # Убираем расширение
                
                # Удалить файлы scaler'а и threshold'а
                for ext in ['.pkl', '_scaler.joblib', '_threshold.joblib']:
                    scaler_path = base_path + ext
                    if os.path.exists(scaler_path):
                        os.remove(scaler_path)
                        
            except Exception as e:
                print(f"Error deleting model files for model {self.id}: {e}")


class DomainTimeLog(db.Model):
    """Сбор продуктивности (домены/сайты)"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    local_ip = db.Column(db.String(50), nullable=False, index=True)
    domain = db.Column(db.String(200), nullable=False, index=True)
    category = db.Column(db.String(50), default='Other')
    duration_seconds = db.Column(db.Integer, default=0)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_user_domain', 'user_id', 'domain'),
    )


class TrafficLog(db.Model):
    """Сбор подозрительных пакетов и сырая активность"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    local_ip = db.Column(db.String(50), nullable=False)
    total_bytes = db.Column(db.BigInteger, default=0)
    packet_count = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_user_ip_time', 'user_id', 'local_ip', 'timestamp'),
    )


class HourlySummary(db.Model):
    """Топология узлов по часам"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hour_timestamp = db.Column(db.DateTime, nullable=False, index=True)
    local_ip = db.Column(db.String(50), nullable=False)
    total_bytes = db.Column(db.BigInteger, default=0)
    packet_count = db.Column(db.Integer, default=0)
    __table_args__ = (db.UniqueConstraint('user_id', 'local_ip', 'hour_timestamp', name='uix_user_ip_hour'),)


class ActiveState(db.Model):
    """Менеджер ML на аккаунт"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    is_monitoring = db.Column(db.Boolean, default=False)
    active_model_id = db.Column(db.Integer, nullable=True)
    interface = db.Column(db.String(100), nullable=True)


class SensorApiKey(db.Model):
    """API ключи для аутентификации сенсоров"""
    __tablename__ = 'sensor_api_keys'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    key_hash = db.Column(db.String(256), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)  # Название сенсора для идентификации
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    user = db.relationship('User', backref=db.backref('api_keys', lazy='dynamic', cascade="all, delete-orphan"))
    
    __table_args__ = (
        db.Index('idx_key_hash', 'key_hash'),
        db.Index('idx_user_active', 'user_id', 'is_active'),
    )