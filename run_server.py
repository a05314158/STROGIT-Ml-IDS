#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для запуска ML-IDS сервера
"""

import os
import sys
from datetime import datetime, timezone
import threading
import time

def run_server():
    """Запуск Flask сервера"""
    try:
        from app import app
        
        # Запуск сервера
        print("Запуск ML-IDS сервера на порту 5000...")
        print("Сервер доступен по адресу: http://localhost:5000")
        print("Для остановки сервера нажмите Ctrl+C\n")
        
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
        
    except ImportError as e:
        print(f"Ошибка импорта приложения: {e}")
        # Если основной импорт не работает, попробуем минимальный запуск
        print("Попытка запустить упрощенную версию сервера...")
        
        # Создаем минимальное Flask приложение для проверки
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/')
        def hello():
            return '''
            <h1>ML-IDS Сервер</h1>
            <p>Система обнаружения вторжений на основе машинного обучения</p>
            <p><a href="/dashboard">Перейти к панели управления</a></p>
            '''
        
        @app.route('/dashboard')
        def dashboard():
            return '<h1>Панель управления ML-IDS</h1><p>Сервис запущен успешно!</p>'
        
        print("Запуск тестового сервера на порту 5000...")
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    run_server()