"""
測試新的 FMP API 端點
"""
import requests
import json

# 測試用 (請替換為您的實際 API key)
TEST_API_KEY = "YOUR_API_KEY_HERE"
TEST_SYMBOL = "AAPL"

# stable API 端點 (當前支援的非 legacy 端點)
url = "https://financialmodelingprep.com/stable/historical-price-eod/full"
params = {
    "symbol": TEST_SYMBOL,
    "apikey": TEST_API_KEY
}

print(f"測試 FMP API 新端點...")
print(f"URL: {url}")
print(f"參數: symbol={TEST_SYMBOL}, apikey=***")
print("-" * 50)

try:
    response = requests.get(url, params=params, timeout=10)
    print(f"狀態碼: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API 調用成功!")
        print(f"數據類型: {type(data)}")
        print(f"數據筆數: {len(data) if isinstance(data, list) else 'N/A'}")
        
        # stable API 返回格式: 直接返回 list
        if isinstance(data, list) and len(data) > 0:
            print(f"\n最新一筆數據範例:")
            print(json.dumps(data[0], indent=2, ensure_ascii=False))
        else:
            print(f"\n完整響應:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"❌ API 調用失敗")
        print(f"響應內容: {response.text}")
        
except Exception as e:
    print(f"❌ 錯誤: {str(e)}")

print("-" * 50)
print("提示: 請將 TEST_API_KEY 替換為您的實際 FMP API key 來進行測試")
