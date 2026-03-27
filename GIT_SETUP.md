# Инструкции по загрузке проекта на GitHub

## Подготовка проекта к загрузке

### 1. Удаление чувствительных данных

Перед загрузкой проекта, убедитесь, что удалены все файлы с чувствительной информацией:

```bash
# Удалите файлы с секретами
rm -f .env
rm -f *.db
rm -f *.db-shm
rm -f *.db-wal
rm -f site.db
rm -f network_ids.db
rm -f network_ids.db-shm
rm -f network_ids.db-wal

# Удалите файлы сессий и кэша
rm -rf __pycache__/
rm -rf .pytest_cache/
rm -rf .venv/
rm -rf venv/
rm -f .env

# Удалите ML-модели, если содержите личную информацию
rm -rf models/
rm -f *.keras
rm -f *.joblib
rm -f *.pkl
rm -f *.h5
```

### 2. Создание .gitignore файла

Создайте файл `.gitignore` в корневой директории проекта:

```
# Виртуальные окружения
.venv/
env/
venv/
ENV/

# Базы данных
*.db
*.db-shm
*.db-wal
network_ids.db
site.db

# Файлы конфигурации
.env
config.json
settings.json
.env.local
.env.development.local
.env.test.local
.env.production.local

# Логи
logs/
*.log
*.log.*

# Кэш
__pycache__/
*.py[cod]
*$py.class
*$pyc
*$pyo
.Python
.pytest_cache/
.coverage
htmlcov/
.cov-report/

# IDE
.vscode/
.idea/
*.swp
*.swo
*.tmp
.DS_Store
Thumbs.db

# OS
.DS_Store
ehthumbs.db
Icon?
desktop.ini

# ML-файлы
*.h5
*.keras
*.joblib
*.pkl
*.sav
models/
test_*.keras
test_*.joblib
test_*.pkl

# Build artifacts
*.so
*.dylib
*.dll

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
xmlresults/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
# JetBrains specific template is maintained in a separate JetBrains.gitignore that can be found at:
# https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
# and can be added to the global gitignore or merged into this file.
.idea/

# VS Code
.vscode/

# Redis dump
dump.rdb

# Temporary files
temp/
tmp/

# Secrets and sensitive data
secret.key
private.key
credentials.json
keys/
passwords/
tokens/

# Custom ML models
model_*.pkl
model_*.joblib
model_*.keras
```

## Загрузка проекта на GitHub

### 1. Откройте командную строку или терминал

Перейдите в директорию проекта:

```bash
cd /путь/к/вашему/проекту/D:/Projects/Ml-ids-main
```

### 2. Инициализируйте локальный репозиторий

```bash
git init
```

### 3. Добавьте файлы к коммиту

```bash
git add .
```

### 4. Создайте первый коммит

```bash
git commit -m "Initial commit: ML-IDS project - Machine Learning Intrusion Detection System"
```

### 5. Создайте репозиторий на GitHub

1. Зайдите на https://github.com
2. Нажмите "New repository"
3. Введите имя репозитория (например, `ml-ids-project` или `ml-intrusion-detection-system`)
4. Добавьте описание:
   ```
   ML-IDS - Machine Learning Intrusion Detection System
   Адаптивная система обнаружения сетевых атак на основе машинного обучения
   ```
5. Выберите "Public" (если хотите, чтобы проект был общедоступным) или "Private"
6. **НЕ** отмечайте "Initialize this repository with a README" (мы уже имеем README.md)
7. Нажмите "Create repository"

### 6. Свяжите локальный репозиторий с удаленным

```bash
# Замените YOUR_USERNAME на ваш никнейм на GitHub
git remote add origin https://github.com/YOUR_USERNAME/ml-ids-project.git

# Или если вы используете SSH:
git remote add origin git@github.com:YOUR_USERNAME/ml-ids-project.git

# Измените ветку по умолчанию на main (если используются современные версии Git)
git branch -M main
```

### 7. Загрузите проект на GitHub

```bash
git push -u origin main
```

## Проверка загрузки

После загрузки проверьте, что:

1. Все файлы проекта находятся в репозитории
2. README.md отображается корректно
3. requirements.txt и setup файлы доступны
4. Нет файлов с чувствительной информацией

## Дополнительные настройки репозитория

После загрузки проекта, на GitHub странице репозитория:

1. Перейдите в "Settings"
2. В "Options" убедитесь, что:
   - Repository visibility установлено правильно (public/private)
   - Включена защита ветки "main" при необходимости
3. В меню "Issues" и "Wiki" включите, если планируете использовать
4. Добавьте темы (topics) для лучшей видимости:
   - ml-ids
   - intrusion-detection
   - machine-learning
   - cybersecurity
   - network-security
   - python
   - flask
   - tensorflow

## Добавление участников (при необходимости)

Если вы хотите добавить других участников:

```bash
# Пригласите участников через GitHub интерфейс
# Settings -> Manage access -> Invite a collaborator
```

## Завершение

Теперь ваш проект ML-IDS успешно загружен на GitHub и готов к использованию другими разработчиками!

## Полезные ссылки

- [GitHub Docs: About remote repositories](https://docs.github.com/en/get-started/getting-started-with-git/about-remote-repositories)
- [GitHub Docs: Adding a remote](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository)
- [GitHub Docs: Managing your repository's settings](https://docs.github.com/en/repositories/managing-your-repository-settings)