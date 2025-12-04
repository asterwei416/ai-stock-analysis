"""
AI 股票趨勢分析系統
使用 Streamlit 框架建立的專業股票技術分析工具
整合 Financial Modeling Prep API 和 Google Gemini AI
"""

import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import google.generativeai as genai

# ==================== 核心函數 ====================

def get_stock_data(symbol, api_key):
    """
    從 Financial Modeling Prep API 獲取股票歷史數據
    
    參數:
        symbol: 股票代碼 (如 AAPL)
        api_key: FMP API 金鑰
    
    返回:
        DataFrame 包含日期、開盤、最高、最低、收盤、成交量
    """
    try:
        # FMP API 端點 - 使用 stable/historical-price-eod/full
        url = "https://financialmodelingprep.com/stable/historical-price-eod/full"
        params = {
            "symbol": symbol,
            "apikey": api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # stable API 直接返回 list 格式
        if not data or not isinstance(data, list) or len(data) == 0:
            st.error(f"❌ 無法找到股票代碼 '{symbol}' 的數據,請確認代碼是否正確")
            return None
        
        # 轉換為 DataFrame
        df = pd.DataFrame(data)
        
        # 檢查並標準化欄位名稱（新 API 可能使用大寫）
        # 將所有欄位名稱轉換為小寫以確保一致性
        df.columns = df.columns.str.lower()
        
        # 確認必要欄位存在
        required_fields = ['date', 'open', 'high', 'low', 'close', 'volume']
        missing_fields = [field for field in required_fields if field not in df.columns]
        
        if missing_fields:
            st.error(f"❌ API 返回的數據缺少必要欄位: {', '.join(missing_fields)}")
            st.info(f"可用欄位: {', '.join(df.columns.tolist())}")
            return None
        
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date", ascending=True).reset_index(drop=True)
        
        return df
    
    except requests.exceptions.Timeout:
        st.error("❌ API 請求超時,請稍後再試")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API 請求失敗: {str(e)}")
        st.info("💡 請確認您的 FMP API Key 是否正確")
        return None
    except Exception as e:
        st.error(f"❌ 數據處理錯誤: {str(e)}")
        return None


def filter_by_date_range(df, start_date, end_date):
    """
    根據日期範圍過濾數據
    
    參數:
        df: 原始數據 DataFrame
        start_date: 起始日期
        end_date: 結束日期
    
    返回:
        過濾後的 DataFrame
    """
    if df is None or df.empty:
        return None
    
    # 確保日期是 datetime 格式
    df["date"] = pd.to_datetime(df["date"])
    
    # 過濾日期範圍
    mask = (df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))
    filtered_df = df[mask].copy()
    
    if filtered_df.empty:
        st.warning("⚠️ 所選日期範圍內沒有數據,請調整日期範圍")
        return None
    
    return filtered_df


def calculate_moving_averages(df):
    """
    計算移動平均線 (MA5, MA10, MA20, MA60)
    
    參數:
        df: 包含股價數據的 DataFrame
    
    返回:
        包含移動平均線欄位的 DataFrame
    """
    if df is None or df.empty:
        return None
    
    # 計算移動平均線
    df["MA5"] = df["close"].rolling(window=5, min_periods=1).mean()
    df["MA10"] = df["close"].rolling(window=10, min_periods=1).mean()
    df["MA20"] = df["close"].rolling(window=20, min_periods=1).mean()
    df["MA60"] = df["close"].rolling(window=60, min_periods=1).mean()
    
    return df


def plot_candlestick_chart(df, symbol):
    """
    繪製專業 K線圖與移動平均線 (Neo-Brutalism 風格)
    
    參數:
        df: 包含股價和移動平均線的 DataFrame
        symbol: 股票代碼
    
    返回:
        Plotly Figure 對象
    """
    # 創建 K線圖
    fig = go.Figure()
    
    # 添加 Candlestick K線圖 (Neo-Brutalism 配色)
    fig.add_trace(go.Candlestick(
        x=df["date"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="K線圖",
        increasing_line_color="#00E676",  # 螢光綠 (上漲)
        increasing_fillcolor="#00E676",
        decreasing_line_color="#FF1744",  # 鮮紅 (下跌)
        decreasing_fillcolor="#FF1744",
        line=dict(width=2)
    ))
    
    # 添加移動平均線 (Neo-Brutalism 高對比配色)
    colors = {
        "MA5": "#FF6B35",   # 活力橙
        "MA10": "#FFD23F",  # 亮黃
        "MA20": "#00B0FF",  # 天藍
        "MA60": "#000000"   # 純黑
    }
    
    for ma_name, color in colors.items():
        if ma_name in df.columns:
            fig.add_trace(go.Scatter(
                x=df["date"],
                y=df[ma_name],
                mode="lines",
                name=ma_name,
                line=dict(color=color, width=3)  # 粗線條
            ))
    
    # 圖表配置
    first_date = df["date"].iloc[0].strftime("%Y-%m-%d")
    last_date = df["date"].iloc[-1].strftime("%Y-%m-%d")
    
    # Neo-Brutalism 風格設定
    fig.update_layout(
        title=dict(
            text=f"<b>{symbol} 股價技術分析</b><br><sub>{first_date} ~ {last_date}</sub>",
            font=dict(
                size=28,
                color="#000000",
                family="Space Grotesk, sans-serif"
            ),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title=dict(
            text="<b>日期</b>",
            font=dict(size=16, color="#000000")
        ),
        yaxis_title=dict(
            text="<b>價格 (USD)</b>",
            font=dict(size=16, color="#000000")
        ),
        plot_bgcolor="#FFFFFF",  # 白色背景
        paper_bgcolor="#FFFFFF",
        height=650,
        hovermode="x unified",
        font=dict(
            family="IBM Plex Mono, monospace",
            size=14,
            color="#000000"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,  # 大幅下移圖例
            xanchor="center",
            x=0.5,
            bgcolor="#FFFFFF",
            bordercolor="#000000",
            borderwidth=3,
            font=dict(size=12, color="#000000")
        ),
        xaxis=dict(
            rangeslider=dict(visible=False),
            type="date",
            showgrid=True,
            gridcolor="#E0E0E0",
            gridwidth=1,
            showline=True,
            linewidth=3,
            linecolor="#000000",
            mirror=True,
            title_standoff=15  # 微調標題距離
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#E0E0E0",
            gridwidth=1,
            showline=True,
            linewidth=3,
            linecolor="#000000",
            mirror=True
        ),
        # 增加更多下邊距以容納圖例
        margin=dict(l=60, r=60, t=140, b=160)
    )
    
    return fig


def generate_ai_analysis(symbol, df, gemini_api_key):
    """
    使用 Google Gemini 2.5 Flash 進行技術分析
    
    參數:
        symbol: 股票代碼
        df: 包含完整交易數據的 DataFrame
        gemini_api_key: Gemini API 金鑰
    
    返回:
        AI 生成的技術分析文本
    """
    try:
        # 配置 Gemini API
        genai.configure(api_key=gemini_api_key)
        
        # 嘗試使用可用的模型
        # 使用 Gemini 2.5 Flash - 用戶指定的先進版本
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
        except Exception as model_error:
            st.error(f"❌ 無法載入 Gemini 模型: {str(model_error)}")
            st.info("💡 請運行 `list_gemini_models.py` 查看您的 API Key 支援的模型")
            return None
        
        # 準備分析數據
        first_date = df["date"].iloc[0].strftime("%Y-%m-%d")
        last_date = df["date"].iloc[-1].strftime("%Y-%m-%d")
        start_price = df["close"].iloc[0]
        end_price = df["close"].iloc[-1]
        price_change = ((end_price - start_price) / start_price) * 100
        
        # 轉換數據為 JSON 格式 (最近 60 筆數據)
        recent_data = df.tail(60).copy()
        recent_data["date"] = recent_data["date"].dt.strftime("%Y-%m-%d")
        data_json = recent_data[["date", "open", "high", "low", "close", "volume", "MA5", "MA10", "MA20", "MA60"]].to_json(
            orient="records", 
            indent=2,
            force_ascii=False
        )
        
        # 構建 AI 提示語
        system_message = """你是一位專業的技術分析師,專精於股票技術分析和歷史數據解讀。你的職責包括:

1. 客觀描述股票價格的歷史走勢和技術指標狀態
2. 解讀歷史市場數據和交易量變化模式
3. 識別技術面的歷史支撐阻力位
4. 提供純教育性的技術分析知識

重要原則:
- 僅提供歷史數據分析和技術指標解讀,絕不提供任何投資建議或預測
- 保持完全客觀中立的分析態度
- 使用專業術語但保持易懂
- 所有分析僅供教育和研究目的
- 強調技術分析的局限性和不確定性
- 使用繁體中文回答

嚴格的表達方式要求:
- 使用「歷史數據顯示」、「技術指標反映」、「過去走勢呈現」等客觀描述
- 避免「可能性」、「預期」、「建議」、「關注」等暗示性用詞
- 禁用「如果...則...」的假設句型,改用「歷史上當...時,曾出現...現象」
- 不提供具體價位的操作參考點,僅描述技術位階的歷史表現
- 強調「歷史表現不代表未來結果」
- 避免任何可能被解讀為操作指引的表達

**格式規範(非常重要):**
- 只使用 ## 標記主要章節標題(如「## 1. 趨勢分析」)
- **絕對不要**在段落內容中使用 # 或 ## 符號
- 段落內容使用純文字或項目符號(-)
- 數字和數據直接寫在段落中,不使用任何標題格式
- 使用 **粗體** 適度強調關鍵詞,但保持文字大小一致
- 避免混用不同的標題級別造成字體大小混亂

免責聲明:所提供的分析內容純粹基於歷史數據的技術解讀,僅供教育和研究參考,不構成任何投資建議或未來走勢預測。歷史表現不代表未來結果。"""
        
        user_prompt = f"""請基於以下股票歷史數據進行深度技術分析:

### 基本資訊
- 股票代號: {symbol}
- 分析期間: {first_date} 至 {last_date}
- 期間價格變化: {price_change:.2f}% (從 ${start_price:.2f} 變化到 ${end_price:.2f})

### 完整交易數據
以下是該期間的完整交易數據,包含日期、開盤價、最高價、最低價、收盤價、成交量和移動平均線:
{data_json}

### 分析要求

請按照以下架構進行分析。**重要:請只使用 ## 標記主要章節,段落內容不要使用任何標題符號**

## 1. 趨勢分析
- 整體趨勢方向(上升、下降、盤整)
- 關鍵支撐位和阻力位識別  
- 趨勢強度評估

## 2. 技術指標分析
- 移動平均線分析(短期與長期MA的關係)
- 價格與移動平均線的相對位置
- 成交量與價格變動的關聯性

## 3. 價格行為分析
- 重要的價格突破點
- 波動性評估
- 關鍵的轉折點識別

## 4. 風險評估  
- 當前價位的風險等級
- 潛在的支撐和阻力區間
- 市場情緒指標

## 5. 市場觀察
- 短期技術面觀察(1-2週)
- 中期技術面觀察(1-3個月)
- 關鍵價位觀察點
- 技術面風險因子

### 輸出格式要求
- 使用 ## 標記主要章節(如上所示)
- **段落內容絕對不使用 # 或 ## 符號,保持文字大小一致**
- 使用項目符號(-)或段落文字組織內容
- 數據和數字直接寫在段落中,不用任何特殊格式包裹
- 使用 **粗體** 適度強調關鍵詞
- 條理清晰,提供具體數據支撐
- 避免過於絕對的預測,強調分析的局限性

分析目標: {symbol}"""
        
        # 調用 Gemini API
        response = model.generate_content(
            [system_message, user_prompt],
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.9,
                max_output_tokens=8192,  # 增加 Token 限制以避免截斷
            ),
            safety_settings={
                genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
            }
        )
        
        # 安全地獲取回應文本
        if response.candidates:
            # 檢查是否有內容部分
            if response.candidates[0].content.parts:
                return response.text
            # 檢查是否因為達到 Token 限制而停止
            elif response.candidates[0].finish_reason == 2: # FinishReason.MAX_TOKENS
                st.warning("⚠️ 分析內容可能因長度限制而被截斷")
                # 嘗試獲取已生成的內容 (如果有)
                try:
                    return response.candidates[0].content.parts[0].text
                except:
                    return "⚠️ 分析生成不完整，請嘗試縮短分析期間或重試。"
            else:
                finish_reason = response.candidates[0].finish_reason
                st.warning(f"⚠️ AI 停止生成，原因代碼: {finish_reason}")
                return None
        else:
            st.warning("⚠️ AI 未返回任何候選回應")
            return None
    
    except Exception as e:
        error_msg = str(e)
        
        # 檢查是否為配額錯誤
        if "429" in error_msg or "quota" in error_msg.lower():
            st.error("❌ Gemini API 配額已超限")
            st.warning("""
            ### 💡 解決方案:
            
            1. **等待配額重置** (通常幾分鐘到1小時)
            2. **升級 API 方案** 到付費版本以獲得更高配額
            3. **檢查使用情況**: [訪問 Gemini API 控制台](https://ai.dev/usage?tab=rate-limit)
            4. **運行模型測試**: 執行 `list_gemini_models.py` 查看可用模型
            
            [了解更多關於配額限制](https://ai.google.dev/gemini-api/docs/rate-limits)
            """)
        else:
            st.error(f"❌ AI 分析失敗: {error_msg}")
            st.info("💡 請確認您的 Gemini API Key 是否正確,並檢查 API 配額")
        
        return None
        
        # 準備分析數據
        first_date = df["date"].iloc[0].strftime("%Y-%m-%d")
        last_date = df["date"].iloc[-1].strftime("%Y-%m-%d")
        start_price = df["close"].iloc[0]
        end_price = df["close"].iloc[-1]
        price_change = ((end_price - start_price) / start_price) * 100
        
        # 轉換數據為 JSON 格式 (最近 60 筆數據)
        recent_data = df.tail(60).copy()
        recent_data["date"] = recent_data["date"].dt.strftime("%Y-%m-%d")
        data_json = recent_data[["date", "open", "high", "low", "close", "volume", "MA5", "MA10", "MA20", "MA60"]].to_json(
            orient="records", 
            indent=2,
            force_ascii=False
        )
        
        # 構建 AI 提示語
        system_message = """你是一位專業的技術分析師,專精於股票技術分析和歷史數據解讀。你的職責包括:

1. 客觀描述股票價格的歷史走勢和技術指標狀態
2. 解讀歷史市場數據和交易量變化模式
3. 識別技術面的歷史支撐阻力位
4. 提供純教育性的技術分析知識

重要原則:
- 僅提供歷史數據分析和技術指標解讀,絕不提供任何投資建議或預測
- 保持完全客觀中立的分析態度
- 使用專業術語但保持易懂
- 所有分析僅供教育和研究目的
- 強調技術分析的局限性和不確定性
- 使用繁體中文回答

嚴格的表達方式要求:
- 使用「歷史數據顯示」、「技術指標反映」、「過去走勢呈現」等客觀描述
- 避免「可能性」、「預期」、「建議」、「關注」等暗示性用詞
- 禁用「如果...則...」的假設句型,改用「歷史上當...時,曾出現...現象」
- 不提供具體價位的操作參考點,僅描述技術位階的歷史表現
- 強調「歷史表現不代表未來結果」
- 避免任何可能被解讀為操作指引的表達

免責聲明:所提供的分析內容純粹基於歷史數據的技術解讀,僅供教育和研究參考,不構成任何投資建議或未來走勢預測。歷史表現不代表未來結果。"""
        
        user_prompt = f"""請基於以下股票歷史數據進行深度技術分析:

### 基本資訊
- 股票代號: {symbol}
- 分析期間: {first_date} 至 {last_date}
- 期間價格變化: {price_change:.2f}% (從 ${start_price:.2f} 變化到 ${end_price:.2f})

### 完整交易數據
以下是該期間的完整交易數據,包含日期、開盤價、最高價、最低價、收盤價、成交量和移動平均線:
{data_json}

### 分析架構:技術面完整分析

#### 1. 趨勢分析
- 整體趨勢方向(上升、下降、盤整)
- 關鍵支撐位和阻力位識別
- 趨勢強度評估

#### 2. 技術指標分析
- 移動平均線分析(短期與長期MA的關係)
- 價格與移動平均線的相對位置
- 成交量與價格變動的關聯性

#### 3. 價格行為分析
- 重要的價格突破點
- 波動性評估
- 關鍵的轉折點識別

#### 4. 風險評估
- 當前價位的風險等級
- 潛在的支撐和阻力區間
- 市場情緒指標

#### 5. 市場觀察
- 短期技術面觀察(1-2週)
- 中期技術面觀察(1-3個月)
- 關鍵價位觀察點
- 技術面風險因子

### 綜合評估要求
#### 輸出格式要求
- 條理清晰,分段論述
- 提供具體的數據支撐
- 避免過於絕對的預測,強調分析的局限性
- 在適當位置使用表格或重點標記

分析目標: {symbol}"""
        
        # 調用 Gemini API
        response = model.generate_content(
            [system_message, user_prompt],
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.9,
                max_output_tokens=4096,
            )
        )
        
        return response.text
    
    except Exception as e:
        st.error(f"❌ AI 分析失敗: {str(e)}")
        st.info("💡 請確認您的 Gemini API Key 是否正確,並檢查 API 配額")
        return None


# ==================== Streamlit 主程式 ====================

def load_neo_brutalism_css():
    """
    載入 Neo-Brutalism 風格的自定義 CSS
    """
    css_path = ".streamlit/neo_brutalism.css"
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Neo-Brutalism CSS 檔案未找到,使用預設樣式")

def main():
    """主程式入口"""
    
    # 頁面配置
    st.set_page_config(
        page_title="AI 股票趨勢分析系統",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 載入 Neo-Brutalism 樣式
    load_neo_brutalism_css()
    
    # 主標題
    st.title("📈 AI 股票趨勢分析系統")
    st.divider()
    
    # ==================== 側邊欄:輸入控制項 ====================
    with st.sidebar:
        st.header("⚙️ 分析設定")
        st.divider()
        
        # 股票代碼輸入
        symbol = st.text_input(
            "📊 股票代碼",
            value="AAPL",
            help="請輸入美股股票代碼,例如: AAPL, MSFT, GOOGL, TSLA"
        ).upper().strip()
        
        # FMP API Key - 優先從 secrets 讀取,否則讓用戶輸入
        try:
            default_fmp_key = st.secrets.get("FMP_API_KEY", "")
        except:
            default_fmp_key = ""
        
        fmp_api_key = default_fmp_key or st.text_input(
            "🔑 FMP API Key",
            type="password",
            help="部署版本已自動配置。本地開發請輸入 Financial Modeling Prep API 金鑰"
        )
        
        # Gemini API Key - 優先從 secrets 讀取,否則讓用戶輸入
        try:
            default_gemini_key = st.secrets.get("GEMINI_API_KEY", "")
        except:
            default_gemini_key = ""
        
        gemini_api_key = default_gemini_key or st.text_input(
            "🤖 Gemini API Key",
            type="password",
            help="部署版本已自動配置。本地開發請輸入 Google Gemini API 金鑰"
        )
        
        # 日期範圍選擇
        st.markdown("### 📅 分析期間")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "起始日期",
                value=datetime.now() - timedelta(days=90),
                help="選擇分析起始日期"
            )
        with col2:
            end_date = st.date_input(
                "結束日期",
                value=datetime.now(),
                help="選擇分析結束日期"
            )
        
        st.divider()
        
        # 開始分析按鈕
        analyze_button = st.button(
            "🚀 開始分析",
            type="primary",
            use_container_width=True
        )
        
        # 免責聲明
        st.divider()
        st.markdown("""
        ### 📢 免責聲明
        本系統僅供學術研究與教育用途,AI 提供的數據與分析結果僅供參考,**不構成投資建議或財務建議**。
        
        請使用者自行判斷投資決策,並承擔相關風險。本系統作者不對任何投資行為負責,亦不承擔任何損失責任。
        
        ---
        
        **API 金鑰註冊**:
        - [FMP API](https://site.financialmodelingprep.com/developer/docs/)
        - [Gemini API](https://aistudio.google.com/app/apikey)
        """)
    
    # ==================== 主要內容區域 ====================
    
    # 輸入驗證
    if analyze_button:
        # 檢查必填欄位
        if not symbol:
            st.error("❌ 請輸入股票代碼")
            st.stop()
        
        if not fmp_api_key:
            st.error("❌ 請輸入 FMP API Key")
            st.info("💡 請前往 [Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs/) 註冊並獲取 API 金鑰")
            st.stop()
        
        if not gemini_api_key:
            st.error("❌ 請輸入 Gemini API Key")
            st.info("💡 請前往 [Google AI Studio](https://aistudio.google.com/app/apikey) 獲取 API 金鑰")
            st.stop()
        
        # 日期驗證
        if start_date >= end_date:
            st.error("❌ 起始日期必須早於結束日期")
            st.stop()
        
        # ==================== 數據獲取 ====================
        with st.spinner(f"📥 正在獲取 {symbol} 的歷史數據..."):
            stock_data = get_stock_data(symbol, fmp_api_key)
        
        if stock_data is None or stock_data.empty:
            st.stop()
        
        st.success(f"✅ 成功獲取 {len(stock_data)} 筆歷史數據")
        
        # ==================== 數據處理 ====================
        with st.spinner("📊 正在處理數據並計算技術指標..."):
            # 過濾日期範圍
            filtered_data = filter_by_date_range(stock_data, start_date, end_date)
            
            if filtered_data is None or filtered_data.empty:
                st.stop()
            
            # 計算移動平均線
            processed_data = calculate_moving_averages(filtered_data)
        
        st.info(f"📈 分析期間: {start_date} ~ {end_date} ({len(processed_data)} 個交易日)")
        
        # ==================== K線圖與技術指標 ====================
        st.header("📊 股價 K線圖與技術指標")
        
        # 繪製圖表
        candlestick_fig = plot_candlestick_chart(processed_data, symbol)
        st.plotly_chart(candlestick_fig, width="stretch")
        
        # ==================== 基本統計資訊 ====================
        st.header("📋 基本統計資訊")
        
        start_price = processed_data["close"].iloc[0]
        end_price = processed_data["close"].iloc[-1]
        price_change = end_price - start_price
        price_change_pct = (price_change / start_price) * 100
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="起始價格",
                value=f"${start_price:.2f}"
            )
        
        with col2:
            st.metric(
                label="結束價格",
                value=f"${end_price:.2f}"
            )
        
        with col3:
            st.metric(
                label="價格變化",
                value=f"${price_change:.2f}",
                delta=f"{price_change_pct:.2f}%"
            )
        
        # ==================== AI 技術分析 ====================
        st.header("🤖 AI 技術分析")
        
        with st.spinner("🧠 AI 正在進行深度技術分析,請稍候..."):
            ai_analysis = generate_ai_analysis(symbol, processed_data, gemini_api_key)
        
        if ai_analysis:
            st.markdown(ai_analysis)
        
        # ==================== 歷史數據表格 ====================
        st.header("📄 歷史數據表格 (最近 10 筆)")
        
        # 顯示最近 10 筆數據
        display_data = processed_data.tail(10).copy()
        display_data = display_data.sort_values("date", ascending=False)
        
        # 格式化顯示欄位
        display_columns = ["date", "open", "high", "low", "close", "volume", "MA5", "MA10", "MA20", "MA60"]
        display_data_formatted = display_data[display_columns].copy()
        
        # 重命名欄位為中文
        display_data_formatted.columns = [
            "日期", "開盤", "最高", "最低", "收盤", "成交量", 
            "MA5", "MA10", "MA20", "MA60"
        ]
        
        st.dataframe(
            display_data_formatted,
            width="stretch",
            hide_index=True
        )
        
        st.success("✅ 分析完成!")


# ==================== 程式執行入口 ====================
if __name__ == "__main__":
    main()
