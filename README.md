# AI 股票趨勢分析系統

一個基於 Streamlit 的專業股票技術分析工具,整合 Financial Modeling Prep API 獲取股票數據,並使用 Google Gemini 2.5 Flash 提供深度 AI 技術分析。

## 🌟 核心功能

- **📊 專業 K線圖**: 使用 Plotly 繪製互動式 K線圖,支援縮放、平移、懸停顯示
- **📈 移動平均線**: 自動計算並顯示 MA5、MA10、MA20、MA60 技術指標
- **🤖 AI 技術分析**: 使用 Gemini 2.5 Flash 進行深度技術面分析
- **📋 數據統計**: 顯示期間價格變化、漲跌幅等關鍵統計資訊
- **📄 歷史數據**: 完整的歷史交易數據表格展示

## 🚀 安裝步驟

### 1. 克隆或下載專案

將專案檔案下載到本地目錄。

### 2. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 3. 獲取 API 金鑰

#### Financial Modeling Prep API Key
1. 前往 [FMP 開發者平台](https://site.financialmodelingprep.com/developer/docs/)
2. 註冊免費帳號
3. 在 Dashboard 中獲取 API Key

#### Google Gemini API Key
1. 前往 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 使用 Google 帳號登入
3. 創建新的 API Key

## 💻 執行方式

在專案目錄下執行:

```bash
streamlit run stock_analysis_app.py
```

系統會自動在瀏覽器開啟網頁應用程式 (預設: http://localhost:8501)

## 📖 使用說明

### 基本操作流程

1. **輸入股票代碼**
   - 在側邊欄輸入美股股票代碼 (如 AAPL, MSFT, GOOGL, TSLA)
   - 系統支援所有在 FMP 數據庫中的美股代碼

2. **設定 API 金鑰**
   - 輸入 FMP API Key (用於獲取股票數據)
   - 輸入 Gemini API Key (用於 AI 分析)

3. **選擇分析期間**
   - 設定起始日期和結束日期
   - 建議至少選擇 30 天以上以獲得更準確的技術分析

4. **開始分析**
   - 點擊「🚀 開始分析」按鈕
   - 系統會依序執行:
     - 獲取股票歷史數據
     - 計算移動平均線
     - 繪製 K線圖
     - 執行 AI 技術分析
     - 顯示數據表格

### 分析結果說明

- **K線圖**: 紅色為上漲,綠色為下跌 (符合亞洲市場習慣)
- **移動平均線**:
  - 金色 (MA5): 5 日短期趨勢
  - 淺紅色 (MA10): 10 日短期趨勢
  - 青色 (MA20): 20 日中期趨勢
  - 紫色 (MA60): 60 日長期趨勢
- **AI 分析**: 包含趨勢分析、技術指標、價格行為、風險評估等深度解讀

## ⚠️ 注意事項

### API 使用限制

- **FMP Free Tier**: 每日 250 次請求限制
- **Gemini API**: 有免費配額限制,詳見 [Google AI 定價](https://ai.google.dev/pricing)

### 數據準確性

- 股票數據來自 Financial Modeling Prep,可能有延遲
- 建議與官方證券交易所數據交叉驗證

### 系統需求

- Python 3.8 或更高版本
- 穩定的網路連線 (用於 API 請求)
- 現代瀏覽器 (Chrome, Firefox, Safari, Edge)

## 🔧 常見問題 FAQ

### Q1: API 請求失敗怎麼辦?

**解決方案**:
- 檢查 API Key 是否正確
- 確認網路連線正常
- 檢查是否超過 API 配額限制
- 確認股票代碼格式正確 (必須是美股代碼)

### Q2: 為什麼圖表沒有顯示?

**解決方案**:
- 確認選擇的日期範圍內有交易數據
- 檢查股票代碼是否正確
- 確認 FMP API 成功返回數據

### Q3: AI 分析沒有顯示?

**解決方案**:
- 檢查 Gemini API Key 是否正確
- 確認 API 配額是否充足
- 查看錯誤訊息以了解具體問題

### Q4: 移動平均線計算不完整?

**說明**:
- MA5 需要至少 5 個交易日
- MA60 需要至少 60 個交易日
- 如果日期範圍過短,長期移動平均線可能不完整

### Q5: 支援台股或其他市場嗎?

**回答**:
- 當前版本僅支援美股
- FMP API 主要提供美股數據
- 如需其他市場,需要更換數據源 API

## 📢 免責聲明

本系統僅供**學術研究與教育用途**。

⚠️ **重要提醒**:
- AI 提供的分析結果僅供參考,**不構成投資建議或財務建議**
- 所有技術分析基於歷史數據,**歷史表現不代表未來結果**
- 投資有風險,請使用者自行判斷投資決策並承擔相關風險
- 本系統作者不對任何投資行為負責,亦不承擔任何損失責任

## 📝 技術架構

- **前端框架**: Streamlit
- **數據來源**: Financial Modeling Prep API
- **AI 模型**: Google Gemini 2.5 Flash
- **視覺化**: Plotly Graph Objects
- **數據處理**: Pandas, NumPy
- **HTTP 請求**: Requests

## 📄 授權

本專案僅供教育和研究使用。

---

**開發者**: Code Gym
**版本**: 1.0.0
**最後更新**: 2025-12-02
