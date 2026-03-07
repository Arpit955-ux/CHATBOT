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
set "REQUESTED_PORT=%FLASK_PORT%"
if "%REQUESTED_PORT%"=="" set "REQUESTED_PORT=5000"

set "FREE_PORT="
for /f %%P in ('powershell -NoProfile -Command "$start=%REQUESTED_PORT%; $max=5100; for($p=$start; $p -le $max; $p++){ try { $l=[System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback,$p); $l.Start(); $l.Stop(); Write-Output $p; break } catch {} }"') do set "FREE_PORT=%%P"

if "%FREE_PORT%"=="" (
  echo Error: no free port available between %REQUESTED_PORT% and 5100.
  exit /b 1
)

if not "%FREE_PORT%"=="%REQUESTED_PORT%" (
  echo Port %REQUESTED_PORT% is busy. Using port %FREE_PORT%.
)

set FLASK_PORT=%FREE_PORT%

echo Starting Quotes Recommendation Chatbot in local NLP mode on http://localhost:%FLASK_PORT%
python app.py
