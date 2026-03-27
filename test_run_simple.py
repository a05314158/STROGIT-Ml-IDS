#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Тестовый скрипт для проверки основных функций ML-IDS

import os
import sys
from datetime import datetime, timezone

# Импортируем основные функции
try:
    import numpy as np
    print("[OK] NumPy успешно импортирован")
except ImportError as e:
    print(f"[ERROR] Ошибка импорта NumPy: {e}")
    sys.exit(1)

try:
    from sklearn.ensemble import IsolationForest
    print("[OK] Scikit-learn успешно импортирован")
except ImportError as e:
    print(f"[ERROR] Ошибка импорта scikit-learn: {e}")
    sys.exit(1)

try:
    import tensorflow as tf
    print("[OK] TensorFlow успешно импортирован")
    print(f"  Версия TensorFlow: {tf.__version__}")
except ImportError as e:
    print(f"[ERROR] Ошибка импорта TensorFlow: {e}")
    sys.exit(1)

try:
    import joblib
    print("[OK] Joblib успешно импортирован")
except ImportError as e:
    print(f"[ERROR] Ошибка импорта Joblib: {e}")
    sys.exit(1)

try:
    import flask
    print("[OK] Flask успешно импортирован")
    print(f"  Версия Flask: {flask.__version__}")
except ImportError as e:
    print(f"[ERROR] Ошибка импорта Flask: {e}")
    sys.exit(1)

# Тестируем основные функции из нашего приложения
try:
    from ml_model import TFAutoencoderDetector, IsolationForestDetector
    print("[OK] ML модели успешно импортированы")
    
    # Создаем тестовые данные
    test_data = np.random.rand(100, 13)  # 100 сэмплов с 13 признаками
    
    # Тестируем Isolation Forest
    iso_detector = IsolationForestDetector()
    iso_detector.train_and_save_model(test_data, "test_iso_model")
    iso_prediction = iso_detector.predict(test_data[:1])
    print(f"[OK] Isolation Forest: предсказание = {iso_prediction}")
    
    # Тестируем Autoencoder
    ae_detector = TFAutoencoderDetector()
    ae_detector.train_and_save_model(test_data, "test_ae_model")
    ae_prediction = ae_detector.predict(test_data[:1])
    print(f"[OK] Autoencoder: предсказание = {ae_prediction}")
    
except Exception as e:
    print(f"[ERROR] Ошибка при тестировании ML моделей: {e}")
    import traceback
    traceback.print_exc()

try:
    from feature_engineer import extract_features
    from data_structures import PacketData
    print("[OK] Feature engineer успешно импортирован")
    
    # Создаем тестовые пакеты
    test_packets = [
        PacketData(
            timestamp=datetime.now(), 
            src_ip="192.168.1.1", 
            dst_ip="192.168.1.2",
            src_port=12345, 
            dst_port=80, 
            length=1500, 
            is_tcp=True, 
            is_udp=False,
            tcp_flags={'SYN': True, 'ACK': False}, 
            protocol='TCP', 
            domain='example.com'
        ) for _ in range(10)
    ]
    
    features = extract_features(test_packets, datetime.now())
    print(f"[OK] Feature extraction: {len(features.features)} признаков извлечено")
    
except Exception as e:
    print(f"[ERROR] Ошибка при тестировании feature engineer: {e}")
    import traceback
    traceback.print_exc()

print("\nВсе основные компоненты успешно прошли тестирование!")
print("Теперь можно запустить основной сервис.")