@echo off
chcp 65001 >nul
echo ========================================
echo   AI 股票趨勢分析系統 - 啟動程式
echo ========================================
echo.

echo [1/3] 檢查 Python 環境...
python --version
if errorlevel 1 (
    echo ❌ 找不到 Python，請先安裝 Python 3.8 或更高版本
    pause
    exit /b 1
)
echo.

echo [2/3] 檢查必要套件...
python -c "import streamlit; import requests; import pandas; import google.generativeai" 2>nul
if errorlevel 1 (
    echo ⚠️  缺少必要套件，開始安裝...
    pip install streamlit requests pandas numpy plotly google-generativeai --quiet
    if errorlevel 1 (
        echo ❌ 套件安裝失敗，請手動執行: pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo ✅ 套件安裝完成
) else (
    echo ✅ 所有套件已安裝
)
echo.

echo [3/3] 啟動 Streamlit 應用程式...
echo.
echo ========================================
echo   系統將在瀏覽器中自動開啟
echo   如果沒有自動開啟，請手動訪問:
echo   http://localhost:8501
echo ========================================
echo.
echo 💡 提示: 按 Ctrl+C 可停止程式
echo.

python -m streamlit run stock_analysis_app.py

pause
