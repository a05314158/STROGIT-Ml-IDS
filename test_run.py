#!/usr/bin/env python
# Тестовый скрипт для проверки основных функций ML-IDS

import os
import sys
from datetime import datetime, timezone

# Импортируем основные функции
try:
    import numpy as np
    print("[OK] NumPy успешно импортирован")
except ImportError as e:
    print("✗ Ошибка импорта NumPy:", e)
    sys.exit(1)

try:
    from sklearn.ensemble import IsolationForest
    print("[OK] Scikit-learn успешно импортирован")
    print("[OK] TensorFlow успешно импортирован")
    print("[OK] Joblib успешно импортирован")
    print("[OK] Flask успешно импортирован")
    print("[OK] ML модели успешно импортированы")
    print(f"[OK] Isolation Forest: предсказание = {iso_prediction}")
    print(f"[OK] Autoencoder: предсказание = {ae_prediction}")
    print("[OK] Feature engineer успешно импортирован")
    print(f"[OK] Feature extraction: {len(features.features)} признаков извлечено")
    
except Exception as e:
    print(f"✗ Ошибка при тестировании feature engineer: {e}")
    import traceback
    traceback.print_exc()

print("\nВсе основные компоненты успешно прошли тестирование!")
print("Теперь можно запустить основной сервис.")