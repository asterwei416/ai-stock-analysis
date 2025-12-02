@echo off
chcp 65001 >nul
echo ========================================
echo   準備部署到 Streamlit Community Cloud
echo ========================================
echo.

echo [步驟 1/4] 檢查 Git 環境...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 找不到 Git，請先安裝 Git
    echo 💡 下載網址: https://git-scm.com/downloads
    pause
    exit /b 1
)
echo ✅ Git 已安裝
echo.

echo [步驟 2/4] 初始化 Git 儲存庫...
if not exist ".git" (
    git init
    echo ✅ Git 儲存庫初始化完成
) else (
    echo ℹ️  Git 儲存庫已存在
)
echo.

echo [步驟 3/4] 添加所有檔案...
git add .
echo ✅ 檔案添加完成
echo.

echo [步驟 4/4] 提交變更...
git commit -m "Initial commit: AI Stock Analysis System" 2>nul
if errorlevel 1 (
    echo ℹ️  沒有新的變更需要提交
) else (
    echo ✅ 提交完成
)
echo.

echo ========================================
echo   下一步：
echo ========================================
echo.
echo 1. 前往 GitHub 創建新的儲存庫:
echo    https://github.com/new
echo.
echo 2. 儲存庫名稱建議: ai-stock-analysis
echo.
echo 3. 執行以下命令連接到遠端儲存庫:
echo    (將 YOUR_USERNAME 替換成您的 GitHub 用戶名)
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/ai-stock-analysis.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. 前往 Streamlit Community Cloud 部署:
echo    https://share.streamlit.io/
echo.
echo ========================================

pause
