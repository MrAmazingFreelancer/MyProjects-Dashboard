@echo off
setlocal
cd /d "%~dp0"
title 7ink Admin - localhost:3000
if not exist "node_modules" (
  echo Installing dependencies...
  call npm install
)
echo Starting 7ink Admin at http://localhost:3000/login
call npm run dev
pause
