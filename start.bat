@echo off
title ribbon-draw

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python wurde nicht gefunden.
    echo Bitte Python von https://www.python.org installieren.
    pause
    exit /b 1
)

python main.py
pause
