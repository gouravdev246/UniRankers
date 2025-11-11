@echo off
call .venv\Scripts\activate
cd unirank
python manage.py runserver 8001
pause
