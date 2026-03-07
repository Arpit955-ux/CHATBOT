@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% neq 0 (
  echo Error: Python is not installed. Install Python 3.10+ and retry.
  exit /b 1
)

if not exist .venv (
  python -m venv .venv
)

call .\.venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt

set FORCE_LOCAL_NLP=1
if "%FLASK_PORT%"=="" set FLASK_PORT=5000

echo Starting Quotes Recommendation Chatbot in local NLP mode on http://localhost:%FLASK_PORT%
python app.py
