@echo off
REM RealTicker Frontend Startup Script for Windows

echo Starting RealTicker Frontend...

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)

REM Check if .env exists
if not exist ".env" (
    echo Creating .env from .env.example...
    copy .env.example .env
)

REM Start the development server
echo Starting React development server...
call npm start
