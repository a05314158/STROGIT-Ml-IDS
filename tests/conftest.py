import pytest
import fakeredis
# Мы импортируем модуль 'app' целиком, чтобы получить доступ к его переменным
import app as app_module
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='session')
def test_app():
    """
    Создает и настраивает экземпляр Flask-приложения для всей тестовой сессии.
    """
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'CELERY_TASK_ALWAYS_EAGER': True,
        'CELERY_TASK_EAGER_PROPAGATES': True,
    })

    # --- КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ ---
    # Мы напрямую заменяем уже созданный r_client на его фейковую In-Memory версию.
    # Это происходит один раз за всю сессию тестов.
    app_module.r_client = fakeredis.FakeRedis(decode_responses=True)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope='function')
def client(test_app):
    """
    Предоставляет тестовый клиент для отправки запросов.
    Автоматически очищает fake_redis перед каждым тестом.
    """
    # Гарантируем, что тесты не влияют друг на друга через Redis
    app_module.r_client.flushall()
    return test_app.test_client()


@pytest.fixture(scope='function')
def test_user(test_app):
    """Создает фейкового пользователя в In-Memory SQLite для тестов."""
    user = User(
        username='CI_Admin_Bot',
        email='ci@enterprise.core',
        password_hash=generate_password_hash('Secur3_T3st_123!')
    )
    db.session.add(user)
    db.session.commit()
    yield user
    db.session.delete(user)
    db.session.commit()