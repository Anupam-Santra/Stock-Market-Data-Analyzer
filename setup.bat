@echo off
REM ============================================================
REM  setup.bat — One-click environment setup for Windows
REM  Run this ONCE before anything else.
REM ============================================================

echo.
echo  ========================================================
echo    Stock Market Data Analyzer — Environment Setup
echo  ========================================================
echo.

REM Check Python
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo  [ERROR] Python not found. Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

echo  [1/4] Creating virtual environment ...
python -m venv venv

echo  [2/4] Activating virtual environment ...
call venv\Scripts\activate.bat

echo  [3/4] Upgrading pip ...
python -m pip install --upgrade pip --quiet

echo  [4/4] Installing dependencies ...
pip install -r requirements.txt

echo.
echo  ========================================================
echo   Setup complete!
echo.
echo   To run the ANALYSIS:
echo     venv\Scripts\activate
echo     python main.py
echo.
echo   To run the DASHBOARD:
echo     venv\Scripts\activate
echo     python dashboard.py
echo     Then open: http://127.0.0.1:8050
echo  ========================================================
echo.
pause
