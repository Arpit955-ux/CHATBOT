@echo off
cd /d "%~dp0"
echo Starting Quotes Recommendation Chatbot with Docker...

where docker >nul 2>nul
if %errorlevel% neq 0 (
  echo Docker not found. Switching to local NLP mode...
  call "%~dp0run_local.bat"
  exit /b %errorlevel%
)

docker info >nul 2>nul
if %errorlevel% neq 0 (
  echo Docker daemon is not running. Switching to local NLP mode...
  call "%~dp0run_local.bat"
  exit /b %errorlevel%
)

set "REQUESTED_WEB_PORT=%WEB_PORT%"
if "%REQUESTED_WEB_PORT%"=="" set "REQUESTED_WEB_PORT=5000"

set "FREE_WEB_PORT="
for /f %%P in ('powershell -NoProfile -Command "$start=%REQUESTED_WEB_PORT%; $max=5100; for($p=$start; $p -le $max; $p++){ try { $l=[System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback,$p); $l.Start(); $l.Stop(); Write-Output $p; break } catch {} }"') do set "FREE_WEB_PORT=%%P"

if "%FREE_WEB_PORT%"=="" (
  echo No free web port available between %REQUESTED_WEB_PORT% and 5100. Switching to local NLP mode...
  call "%~dp0run_local.bat"
  exit /b %errorlevel%
)

if not "%FREE_WEB_PORT%"=="%REQUESTED_WEB_PORT%" (
  echo Port %REQUESTED_WEB_PORT% is busy. Docker web UI will use http://localhost:%FREE_WEB_PORT%
)
set WEB_PORT=%FREE_WEB_PORT%

docker compose version >nul 2>nul
if %errorlevel% equ 0 (
  docker compose up --build
  exit /b %errorlevel%
)

where docker-compose >nul 2>nul
if %errorlevel% equ 0 (
  docker-compose up --build
  exit /b %errorlevel%
)

echo Docker Compose is not available. Switching to local NLP mode...
call "%~dp0run_local.bat"
exit /b %errorlevel%
