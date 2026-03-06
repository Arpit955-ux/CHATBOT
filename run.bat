@echo off
echo Starting Quotes Recommendation Chatbot with Docker...

where docker >nul 2>nul
if %errorlevel% neq 0 (
  echo Error: Docker is not installed. Install Docker Desktop first.
  exit /b 1
)

docker info >nul 2>nul
if %errorlevel% neq 0 (
  echo Error: Docker daemon is not running. Start Docker Desktop and retry.
  exit /b 1
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

echo Error: Docker Compose is not available.
echo Install Docker Compose plugin or docker-compose.
exit /b 1
