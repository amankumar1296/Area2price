@echo off
cd /d "%~dp0"
title House Price Predictor UI
echo ========================================================
echo  Launching House Price Prediction Web UI
echo  AI/ML Foundations - Session 21
echo ========================================================
echo.
echo Starting Flask web server at http://localhost:5000 ...
echo Press Ctrl+C in this window to stop the server anytime.
echo.

:: Launch browser in background after 2 seconds to allow Flask to bind
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:5000"

:: Run Flask app with python or py launcher
where python >nul 2>nul
if %errorlevel% equ 0 (
    python app.py
) else (
    py -3 app.py
)

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to run app.py. Please make sure Python and required libraries are installed.
    echo Run: pip install flask numpy pandas scikit-learn matplotlib
)
pause
