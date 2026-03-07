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
