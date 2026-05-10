@echo off
REM ============================================================
REM  run_dashboard.bat — Launch the enterprise Dash dashboard
REM ============================================================
call venv\Scripts\activate.bat
echo.
echo  Starting Enterprise Dashboard ...
echo  Open your browser at: http://127.0.0.1:8050
echo  Press Ctrl+C to stop.
echo.
python dashboard.py
pause
