@echo off
chcp 65001 >nul
REM Chay file nay trong thu muc G:\django\taskmanager_project
cd /d "%~dp0"

echo === 1. Tao moi truong ao venv ===
python -m venv venv

echo === 2. Kich hoat venv ===
call venv\Scripts\activate.bat

echo === 3. Cai Django ===
python -m pip install --upgrade pip
pip install django
python -m django --version
pip freeze > requirements.txt

echo === 4. Tao migration va migrate ===
cd taskmanager
python manage.py makemigrations tasks
python manage.py migrate

echo === 5. Tao superuser (nhap username / email / password) ===
python manage.py createsuperuser

echo === 6. Chay server: http://127.0.0.1:8000/ ===
python manage.py runserver
