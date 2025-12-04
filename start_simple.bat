@echo off
chcp 65001 >nul
echo ========================================
echo   AI 股票趨勢分析系統 - 簡易啟動
echo ========================================
echo.
echo 正在啟動 Streamlit...
echo.

cd /d "%~dp0"
python -m streamlit run stock_analysis_app.py

echo.
pause
