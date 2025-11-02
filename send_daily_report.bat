@echo off
cd /d E:\AI
call venv\Scripts\activate
python manage.py send_daily_report --force