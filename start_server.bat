@echo off
echo Запуск ML-IDS сервера...
python -c "from app import app; app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)"
pause