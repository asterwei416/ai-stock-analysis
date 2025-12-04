# AI 股價分析系統 規格說明書 v2

> **版本說明**: v2 (2025-12-04 更新) - 整合 Neo-Brutalism 設計風格、FMP API v3/Stable 端點修正、Gemini 2.5 Flash 模型優化及穩健性增強。

## 📋 系統概述

### 系統名稱
【Code Gym】AI 股票趨勢分析系統 (v2)

### 核心功能描述
建立一個基於網頁的股票技術分析工具，能夠：
1. 獲取指定股票的歷史價格數據和技術指標
2. 繪製專業的K線圖和移動平均線圖表 (Neo-Brutalism 風格)
3. 使用 Google Gemini 2.5 Flash AI 進行深度技術面分析和趨勢解讀
4. 提供客觀的歷史數據分析和教育性技術指標說明

### 技術架構要求
- **界面框架**: 使用 Streamlit 框架
- **設計風格**: **Neo-Brutalism (新野獸派)** - 高對比度、粗實邊框、硬朗陰影
- **數據來源**: Financial Modeling Prep (FMP) API (Stable Endpoint)
- **AI 模型**: **Google Gemini 2.5 Flash**
- **視覺化工具**: 互動式圖表 (使用 Plotly Graph Objects)
- **數據處理**: Pandas, NumPy, Pyarrow
- **HTTP請求**: requests
- **日期處理**: datetime
- **部署方式**: 本地運行 (附帶端口自動清理腳本)

## 🎯 功能需求規格

### F-001: 用戶界面設計 (Neo-Brutalism)
**設計風格要求**:
- **配色方案**: 
  - 主色調: 黃色 (#FFD23F)
  - 輔助色: 橙色 (#FF6B35)
  - 邊框/文字: 純黑 (#000000)
  - 背景/卡片: 純白 (#FFFFFF)
- **視覺元素**:
  - 所有容器、按鈕、輸入框均需有 **3-4px 黑色粗實邊框**
  - 元素需有 **黑色硬朗陰影 (Hard Shadow)**，不使用模糊陰影
  - 字體: 使用 `Space Grotesk` (標題) 和 `IBM Plex Mono` (內文/代碼)
- **側邊欄**:
  - 背景色: 黃色 (#FFD23F)
  - **收合按鈕**: 必須**強制始終顯示** (不依賴懸停)，並使用自定義黑色箭頭圖標，隱藏預設文字
  - **輸入框**: 白色背景，黑色邊框
  - **密碼輸入框**: 必須確保「顯示密碼」的眼睛圖標為黑色可見

**基本佈局**: 
- 頁面標題: "AI 股票趨勢分析系統"
- 左側控制區包含：
  - 股票代碼輸入 (預設: "AAPL")
  - FMP API Key (Password type)
  - Gemini API Key (Password type)
  - 日期範圍選擇

### F-002: 數據獲取功能
**API 端點更新**:
- 使用 FMP Stable Endpoint: `https://financialmodelingprep.com/stable/historical-price-eod/full`
- 參數: `symbol`, `apikey`
- 錯誤處理: 需妥善處理 API 連線失敗、無效代碼、數據欄位缺失等情況

### F-003: 數據處理與計算
**計算項目**:
- MA5, MA10, MA20, MA60 移動平均線
- 需處理 `pyarrow` 依賴問題 (確保 requirements.txt 包含 pyarrow)

### F-004: 主要顯示區域設計
**圖表設計 (Plotly)**:
- **風格**: 配合 Neo-Brutalism 風格
  - 背景: 白色
  - 網格線: 黑色或深灰色，粗線條
  - 邊框: 圖表區域需有粗黑色邊框
- **佈局優化**:
  - **邊距 (Margins)**: 上下邊距需足夠大 (Top: 140px+, Bottom: 160px+)，避免標題與標籤壓到邊框
  - **圖例 (Legend)**: 必須放置在圖表下方且**大幅下移** (y=-0.4)，避免與 X 軸標題 ("日期") 重疊
  - **X 軸標題**: 需設定 `standoff` 距離，避免貼近軸線

### F-005: 基本資訊展示
- 使用 Neo-Brutalism 風格的指標卡片 (白色背景、黑色邊框、硬陰影)

### F-006: AI分析功能 (Gemini 2.5 Flash)
**模型設定**:
- 模型: `gemini-2.5-flash`
- 參數: 
  - `temperature`: 0.7
  - `max_output_tokens`: **8192** (防止長文截斷)
- **安全設定**: 將所有安全過濾器 (Harassment, Hate Speech, etc.) 設為 `BLOCK_NONE` 以避免誤判阻擋分析

**錯誤處理增強**:
- **Token 截斷處理**: 若 API 返回 `finish_reason: 2 (MAX_TOKENS)`，系統不應崩潰，而應嘗試顯示已生成的內容，並顯示警告訊息 ("分析內容可能因長度限制而被截斷")
- **配額限制處理**: 若遇 429 錯誤，顯示友善的配額超限提示

**提示詞 (Prompt) 優化**:
- 角色: 專業技術分析師
- 格式: 嚴格限制使用 Markdown 標題 (僅允許 ##)，避免字體大小混亂
- 內容: 客觀、教育性、繁體中文

### F-007: 輔助功能
- **啟動腳本 (`start.bat`)**:
  - 必須包含自動檢測並**終止佔用 8501 端口**的進程的邏輯 (`netstat`, `taskkill`)
  - 確保每次啟動都能成功運行 Streamlit

## 🎨 界面設計與體驗標準 (v2 更新)
- **視覺衝擊力**: 透過高對比配色和粗框線創造強烈的視覺印象
- **可讀性**: 確保在強烈風格下，文字和數據依然清晰可讀 (特別是側邊欄文字顏色)
- **互動性**: 按鈕和輸入框在懸停/點擊時應有位移效果 (Translate)，模擬實體按鍵回饋

## 📊 品質標準
- **穩健性**: AI 分析失敗時不應導致整個應用程式崩潰
- **完整性**: 圖表標題、標籤、圖例不得互相重疊或被裁切
- **易用性**: 側邊欄收合按鈕必須隨時可見，方便用戶切換全螢幕查看圖表

## 📂 交付物要求
**最終交付物**: 
1. `stock_analysis_app.py`: 主程式 (包含 CSS 注入、API 邏輯、圖表繪製)
2. `.streamlit/neo_brutalism.css`: 獨立的 CSS 樣式文件
3. `start.bat`: 包含端口清理功能的啟動腳本
4. `requirements.txt`: 包含 `streamlit`, `pandas`, `plotly`, `google-generativeai`, `requests`, `pyarrow`
5. `list_gemini_models.py`: 用於檢查可用模型的工具腳本
