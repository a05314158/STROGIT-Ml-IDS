# Загрузка проекта ML-IDS на GitHub

## Шаги для загрузки проекта на GitHub

### 1. Подготовка проекта

Прежде чем загружать проект, убедитесь, что вы удалили все чувствительные данные:

```bash
# Удалите файлы с секретами
rm -f .env
rm -f *.db
rm -f *.db-shm
rm -f *.db-wal

# Удалите файлы сессий и кэша
rm -rf __pycache__/
rm -rf .pytest_cache/
rm -rf .venv/
rm -rf .env
```

### 2. Удалите чувствительные данные из истории коммитов (если были)

Если ранее в истории коммитов были чувствительные данные, удалите их:

```bash
# Удаление чувствительных файлов из всей истории
git filter-branch --force --index-filter \
"git rm --cached --ignore-unmatch PATH-TO-YOUR-FILE" \
--prune-empty --tag-name-filter cat -- --all
```

### 3. Инициализация Git репозитория

```bash
# Перейдите в директорию проекта
cd /путь/к/вашему/проекту

# Инициализируйте локальный репозиторий
git init

# Добавьте все файлы к коммиту
git add .
```

### 4. Создайте .gitignore файл

Создайте файл `.gitignore` в корневой директории проекта:

```
# Виртуальные окружения
.venv/
env/
venv/

# Базы данных
*.db
*.db-shm
*.db-wal

# Файлы конфигурации
.env
config.json
settings.json

# Логи
logs/
*.log

# Кэш
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.pytest_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# ML-файлы
*.h5
*.keras
*.joblib
*.pkl
*.sav
models/
```

### 5. Создайте коммит

```bash
# Создайте первый коммит
git add .
git commit -m "Initial commit: ML-IDS project"
```

### 6. Создайте репозиторий на GitHub

1. Зайдите на https://github.com
2. Нажмите "New repository"
3. Введите имя репозитория (например, `ml-ids-project`)
4. Добавьте описание
5. Выберите "Public" или "Private" (в зависимости от ваших предпочтений)
6. **НЕ** отмечайте "Initialize this repository with a README"
7. Нажмите "Create repository"

### 7. Свяжите локальный репозиторий с удаленным

```bash
# Добавьте удаленный репозиторий
git remote add origin https://github.com/ВАШ_АККАУНТ/ml-ids-project.git

# Измените ветку по умолчанию на main (если используется новая версия Git)
git branch -M main
```

### 8. Загрузите проект на GitHub

```bash
# Загрузите коммиты на GitHub
git push -u origin main
```

### 9. Создайте README.md для репозитория

После успешной загрузки добавьте информативный README.md файл в корень репозитория:

```markdown
# ML-IDS - Machine Learning Intrusion Detection System

## Описание
ML-IDS - это система обнаружения сетевых атак на основе машинного обучения. Система анализирует сетевой трафик в режиме реального времени и выявляет аномалии, которые могут свидетельствовать о попытках взлома или несанкционированного доступа.

## Архитектура
- Веб-интерфейс на Flask
- ML-модели на TensorFlow и Scikit-Learn
- Сенсоры для захвата пакетов
- Система анализа признаков
- Интерфейс для управления моделями и API-ключами

## Установка
1. Установите зависимости: `pip install -r requirements.txt`
2. Запустите сервер: `python app.py`
3. Запустите сенсор: `python sensor.py --server localhost --apikey <your_api_key> --iface <interface>`

## Использование
1. Зарегистрируйтесь в веб-интерфейсе
2. Создайте API-ключ для сенсора
3. Запустите сенсор на нужном интерфейсе
4. Обучите модель на нормальных данных
5. Активируйте модель для мониторинга
```

### 10. (Опционально) Добавьте лицензию

Создайте файл `LICENSE` в корневой директории:

```
MIT License

Copyright (c) 2026 ML-IDS Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Теперь ваш проект успешно загружен на GitHub!

## Альтернативный способ через GitHub Desktop

1. Установите GitHub Desktop
2. Авторизуйтесь с вашими GitHub учетными данными
3. Выберите "Add an Existing Repository from your Hard Drive..."
4. Найдите папку с проектом
5. Нажмите "Publish repository"
6. Задайте имя репозитория и настройки
7. Нажмите "Publish"

## Важные замечания

- Не загружайте файлы с чувствительной информацией (ключи, пароли, конфигурации)
- Убедитесь, что в репозитории нет личных данных
- Обновите все документы перед загрузкой
- Проверьте, что все зависимости правильно указаны в requirements.txt