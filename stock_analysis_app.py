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
        # FMP API 端點 - 獲取完整歷史數據
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}"
        params = {"apikey": api_key}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # 檢查 API 回應
        if "historical" not in data:
            st.error(f"❌ 無法找到股票代碼 '{symbol}' 的數據,請確認代碼是否正確")
            return None
        
        # 轉換為 DataFrame
        df = pd.DataFrame(data["historical"])
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
    繪製專業 K線圖與移動平均線
    
    參數:
        df: 包含股價和移動平均線的 DataFrame
        symbol: 股票代碼
    
    返回:
        Plotly Figure 對象
    """
    # 創建 K線圖
    fig = go.Figure()
    
    # 添加 Candlestick K線圖
    fig.add_trace(go.Candlestick(
        x=df["date"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="K線圖",
        increasing_line_color="#FF4B4B",  # 上漲為紅色
        decreasing_line_color="#00CC96",  # 下跌為綠色
    ))
    
    # 添加移動平均線
    colors = {
        "MA5": "#FFD700",   # 金色
        "MA10": "#FF6B6B",  # 淺紅色
        "MA20": "#4ECDC4",  # 青色
        "MA60": "#A78BFA"   # 紫色
    }
    
    for ma_name, color in colors.items():
        if ma_name in df.columns:
            fig.add_trace(go.Scatter(
                x=df["date"],
                y=df[ma_name],
                mode="lines",
                name=ma_name,
                line=dict(color=color, width=2)
            ))
    
    # 圖表配置
    first_date = df["date"].iloc[0].strftime("%Y-%m-%d")
    last_date = df["date"].iloc[-1].strftime("%Y-%m-%d")
    
    fig.update_layout(
        title=f"{symbol} 股價 K線圖與技術指標 ({first_date} ~ {last_date})",
        xaxis_title="日期",
        yaxis_title="價格 (USD)",
        template="plotly_white",
        height=600,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            rangeslider=dict(visible=False),
            type="date"
        )
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
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        
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

def main():
    """主程式入口"""
    
    # 頁面配置
    st.set_page_config(
        page_title="AI 股票趨勢分析系統",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
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
        st.plotly_chart(candlestick_fig, use_container_width=True)
        
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
            use_container_width=True,
            hide_index=True
        )
        
        st.success("✅ 分析完成!")


# ==================== 程式執行入口 ====================
if __name__ == "__main__":
    main()
