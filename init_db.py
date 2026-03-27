#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт инициализации базы данных для ML-IDS
"""

import os
from app import app, db
from models import User

def init_database():
    """Инициализация базы данных"""
    with app.app_context():
        # Создание всех таблиц
        db.create_all()
        print("Таблицы созданы успешно")
        
        # Проверка, есть ли пользователи
        user_count = User.query.count()
        print(f"Количество пользователей в базе: {user_count}")
        
        if user_count == 0:
            # Создание тестового пользователя
            from werkzeug.security import generate_password_hash
            test_user = User(
                username="admin",
                email="admin@ml-ids.local",
                password_hash=generate_password_hash("admin123")
            )
            db.session.add(test_user)
            db.session.commit()
            print("Создан тестовый пользователь: admin / admin123")
        else:
            print("Пользователи уже существуют в базе данных")

if __name__ == "__main__":
    init_database()