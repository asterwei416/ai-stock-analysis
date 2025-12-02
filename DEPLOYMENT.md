# Streamlit Community Cloud 部署指南

本指南將引導您將 AI 股票趨勢分析系統部署到 Streamlit Community Cloud,讓全世界都能訪問您的應用!

## 📋 部署前準備

### 1. 準備 GitHub 帳號和儲存庫

#### 1.1 創建 GitHub 帳號
- 前往 [GitHub](https://github.com/) 註冊帳號(如果還沒有)

#### 1.2 創建新的儲存庫
```
1. 登入 GitHub
2. 點擊右上角 "+" → "New repository"
3. 填寫資訊:
   - Repository name: ai-stock-analysis
   - Description: AI 股票趨勢分析系統
   - Public (公開) 或 Private (私有) - 兩者都可以
4. 勾選 "Add a README file"
5. 點擊 "Create repository"
```

#### 1.3 將專案上傳到 GitHub

**方式 1 - 使用 Git 命令列** (推薦):
```bash
# 在專案目錄下執行
cd "c:\Users\trist\Desktop\Google Antigravity\AI股票趨勢分析系統"

# 初始化 Git
git init

# 添加所有檔案
git add .

# 提交
git commit -m "Initial commit: AI Stock Analysis System"

# 連接到遠端儲存庫 (替換成您的儲存庫網址)
git remote add origin https://github.com/您的用戶名/ai-stock-analysis.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

**方式 2 - 使用 GitHub Desktop**:
1. 下載並安裝 [GitHub Desktop](https://desktop.github.com/)
2. File → Add Local Repository → 選擇專案資料夾
3. Publish repository 到 GitHub

### 2. 準備 Streamlit Community Cloud 帳號

1. 前往 [Streamlit Community Cloud](https://share.streamlit.io/)
2. 點擊 "Sign up" 或 "Continue with GitHub"
3. 使用 GitHub 帳號登入
4. 授權 Streamlit 訪問您的 GitHub 儲存庫

---

## 🚀 部署步驟

### Step 1: 登入 Streamlit Community Cloud

1. 前往 https://share.streamlit.io/
2. 使用 GitHub 帳號登入

### Step 2: 創建新的應用

1. 點擊 "New app" 按鈕
2. 填寫部署資訊:
   - **Repository**: 選擇您的 `ai-stock-analysis` 儲存庫
   - **Branch**: `main` (或您的主要分支)
   - **Main file path**: `stock_analysis_app.py`
3. 點擊 "Advanced settings" (可選)
   - 可以設定自訂網域
   - 選擇 Python 版本

### Step 3: 配置 Secrets (重要!)

由於應用需要 API 金鑰,我們需要安全地配置 secrets:

1. 在 Streamlit Cloud 部署頁面,點擊 "Advanced settings"
2. 找到 "Secrets" 區塊
3. 貼上以下內容 (替換成您的真實 API Key):

```toml
# .streamlit/secrets.toml
# 警告: 切勿將此檔案上傳到 GitHub!

# Financial Modeling Prep API Key
FMP_API_KEY = "your_fmp_api_key_here"

# Google Gemini API Key  
GEMINI_API_KEY = "your_gemini_api_key_here"
```

4. 點擊 "Save"

### Step 4: 部署!

1. 點擊 "Deploy!" 按鈕
2. 等待部署完成 (通常需要 2-5 分鐘)
3. 部署成功後,您會獲得一個公開網址,如:
   ```
   https://您的用戶名-ai-stock-analysis.streamlit.app
   ```

---

## 🔒 安全性考量

### ⚠️ 重要: 保護您的 API 金鑰

**絕對不要**將包含真實 API 金鑰的檔案上傳到 GitHub!

#### 創建 .gitignore 檔案

在專案根目錄創建 `.gitignore` 檔案:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual Environment
venv/
env/
ENV/

# Streamlit
.streamlit/secrets.toml

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

這樣可以確保 secrets.toml 不會被上傳到 GitHub。

---

## 🔧 修改應用以支援 Secrets

### 更新 stock_analysis_app.py

為了支援從 Streamlit Secrets 讀取 API 金鑰,需要修改程式碼:

**原本的輸入方式**:
```python
fmp_api_key = st.text_input("🔑 FMP API Key", type="password")
gemini_api_key = st.text_input("🤖 Gemini API Key", type="password")
```

**修改為**:
```python
# 優先從 secrets 讀取,如果沒有則讓用戶輸入
fmp_api_key = st.secrets.get("FMP_API_KEY", "") or st.text_input(
    "🔑 FMP API Key", 
    type="password",
    help="本地使用請輸入 API Key"
)

gemini_api_key = st.secrets.get("GEMINI_API_KEY", "") or st.text_input(
    "🤖 Gemini API Key", 
    type="password",
    help="本地使用請輸入 API Key"
)
```

這樣做的好處:
- ✅ 部署到 Cloud 時自動使用 secrets 中的 API Key
- ✅ 本地開發時仍可手動輸入
- ✅ 用戶訪問您的應用時不需要輸入 API Key

---

## 📱 部署後管理

### 查看應用狀態

1. 登入 https://share.streamlit.io/
2. 在 Dashboard 中可以看到:
   - 應用運行狀態
   - 訪問次數統計
   - 日誌輸出
   - 錯誤訊息

### 更新應用

當您修改程式碼並推送到 GitHub 後:
1. Streamlit Cloud 會自動檢測更新
2. 自動重新部署應用
3. 或者手動點擊 "Reboot app" 強制重啟

### 停止或刪除應用

在 Dashboard 中:
- 點擊應用旁的 "..." 選單
- 選擇 "Delete app" 即可刪除

---

## 🌟 最佳實踐

### 1. 使用環境變數

將敏感資訊都存放在 Streamlit Secrets 中,不要硬編碼在程式中。

### 2. 設定使用限制

如果擔心 API 配額被用完,可以考慮:
- 為應用設定密碼保護
- 限制可分析的日期範圍
- 添加每日使用次數限制

### 3. 優化效能

- 使用 `@st.cache_data` 快取數據
- 減少不必要的 API 調用
- 優化圖表渲染

### 4. 監控使用情況

定期檢查:
- API 使用量
- 應用訪問次數
- 錯誤日誌

---

## ❓ 常見問題

### Q1: 部署失敗怎麼辦?

**解決方案**:
1. 檢查 `requirements.txt` 是否正確
2. 查看部署日誌找出錯誤訊息
3. 確認所有依賴套件都可以在 Linux 環境編譯
4. 如果是 pyarrow 問題,可以在 requirements.txt 中移除

### Q2: API 金鑰洩露了怎麼辦?

**立即行動**:
1. 到 FMP 和 Gemini 官網撤銷舊的 API Key
2. 生成新的 API Key
3. 在 Streamlit Cloud Secrets 中更新
4. 檢查 GitHub 儲存庫歷史,確保沒有 API Key 被提交

### Q3: 如何讓應用更快?

**優化建議**:
```python
# 使用 cache 快取股票數據
@st.cache_data(ttl=3600)  # 快取 1 小時
def get_stock_data(symbol, api_key):
    # ... 您的程式碼
```

### Q4: 可以使用自訂網域嗎?

免費版 Streamlit Community Cloud 不支援自訂網域。
如需自訂網域,可以考慮:
- Streamlit for Teams (付費方案)
- 使用其他雲端部署平台 (如 Heroku, AWS)

---

## 📚 相關資源

- [Streamlit Community Cloud 官方文件](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Secrets 管理](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [部署教學影片](https://www.youtube.com/watch?v=HKoOBiAaHGg)

---

## 🎉 完成!

部署成功後,您就可以:
- 📤 分享應用網址給朋友、同事
- 📊 讓任何人都能使用您的 AI 股票分析工具
- 🌍 將專案加入履歷或作品集

**祝您部署順利!** 🚀
