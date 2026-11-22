@echo off
cd /d "%~dp0"
title House Price Prediction ML Pipeline
echo ========================================================
echo  Running House Price Prediction (AI/ML Foundations)
echo ========================================================
echo.
echo Note: Matplotlib graph windows will open during execution.
echo Close each plot window to proceed to the next step.
echo.

where python >nul 2>nul
if %errorlevel% equ 0 (
    python house_price_prediction.py
) else (
    py -3 house_price_prediction.py
)

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to run house_price_prediction.py.
    echo Run: pip install numpy pandas scikit-learn matplotlib
)
echo.
pause
