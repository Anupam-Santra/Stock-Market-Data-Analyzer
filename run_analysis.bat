@echo off
REM ============================================================
REM  run_analysis.bat — Run the full analysis pipeline
REM ============================================================
call venv\Scripts\activate.bat
echo.
echo  Running Stock Market Analysis ...
echo.
python main.py
echo.
echo  Done! Check outputs\charts\ and reports\
pause
