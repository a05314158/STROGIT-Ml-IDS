from config import NUM_FEATURES


def test_api_rejects_empty_payload(client):
    """Проверка защиты: Сервер не должен падать с 500 ошибкой при сбое датчика"""
    res = client.post('/api/sensor_data', json={})
    assert res.status_code == 400
    assert "Blank Stream" in res.json['msg']


def test_api_rejects_unregistered_sensors(client):
    """Zero-Trust: Запрещаем слив данных с неизвестных аккаунтов-email"""
    res = client.post('/api/sensor_data', json={
        "email": "hacker@evil.org",
        "features": [0.0] * NUM_FEATURES
    })
    assert res.status_code == 403


def test_api_accepts_valid_payload(client, test_user):
    """Корректная интеграция Сенсора с Мозгом и Атомарный инсерт"""
    payload = {
        "email": "ci@enterprise.core",
        "features": [1.5, 0.0, 3.2] + [0.0] * (NUM_FEATURES - 3),
        "packet_count": 55,
        "total_bytes": 1024,
        "ip_summary": {"192.168.1.15": 1024},
        "domain_summary": {"github.com": 20, "tls.handshake": 1}
    }

    res = client.post('/api/sensor_data', json=payload)

    assert res.status_code == 202
    assert res.json['status'] == "Accepted"
    # Благодаря EAGER режиму в Celery, предсказания AI уже вызвались, ошибок нет.


def test_api_vector_shape_defense(client, test_user):
    """AI Defense: TensorFlow умрет, если подать массив с длиной != NUM_FEATURES (13)."""
    payload = {
        "email": "ci@enterprise.core",
        "features": [0.5, 0.6],  # Недостоверный огрызок вектора из 2 цифр
    }
    res = client.post('/api/sensor_data', json=payload)
    assert res.status_code == 422  # 422 Unprocessable Entity