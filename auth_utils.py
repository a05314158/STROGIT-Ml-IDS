"""
Утилиты для аутентификации сенсоров через API Keys
"""
import secrets
import hashlib
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


def generate_api_key() -> str:
    """Генерирует криптографически стойкий API ключ"""
    return secrets.token_urlsafe(32)


def hash_api_key(api_key: str) -> str:
    """Хеширует API ключ для безопасного хранения в БД"""
    return generate_password_hash(api_key, method='scrypt')


def verify_api_key(api_key: str, key_hash: str) -> bool:
    """Проверяет API ключ против хеша"""
    return check_password_hash(key_hash, api_key)


def validate_api_key_from_request(request, db_session):
    """
    Валидирует API ключ из HTTP запроса.
    
    Returns:
        User object если ключ валиден, None если нет
    """
    from models import SensorApiKey, User
    
    # Проверяем заголовок Authorization
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    # Формат: "Bearer <api_key>"
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    
    api_key = parts[1]
    
    # Ищем активные ключи
    active_keys = SensorApiKey.query.filter_by(is_active=True).all()
    
    for key_record in active_keys:
        if verify_api_key(api_key, key_record.key_hash):
            # Обновляем время последнего использования
            key_record.last_used = datetime.utcnow()
            db_session.commit()
            
            # Возвращаем пользователя
            return User.query.get(key_record.user_id)
    
    return None
