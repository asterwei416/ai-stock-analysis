"""
調試腳本：檢查 FMP API 實際返回的數據結構
"""
import requests
import json

# 請替換為您的 API key
API_KEY = "YOUR_API_KEY_HERE"
SYMBOL = "AAPL"

# stable API 端點 (當前支援的非 legacy 端點)
url = "https://financialmodelingprep.com/stable/historical-price-eod/full"
params = {
    "symbol": SYMBOL,
    "apikey": API_KEY
}

print("調試 FMP API 響應格式...")
print("=" * 60)

try:
    response = requests.get(url, params=params, timeout=10)
    print(f"狀態碼: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"數據類型: {type(data)}")
        print(f"數據筆數: {len(data) if isinstance(data, list) else 'N/A'}\n")
        
        # stable API 返回格式: 直接返回 list
        if isinstance(data, list) and len(data) > 0:
            print("=" * 60)
            print("第一筆數據的所有欄位:")
            print("=" * 60)
            first_record = data[0]
            for key, value in first_record.items():
                print(f"  {key}: {value} (type: {type(value).__name__})")
            
            print("\n" + "=" * 60)
            print("完整第一筆數據 JSON:")
            print("=" * 60)
            print(json.dumps(first_record, indent=2, ensure_ascii=False))
        else:
            print("完整響應:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"錯誤狀態碼: {response.status_code}")
        print(f"響應內容: {response.text}")
        
except Exception as e:
    print(f"❌ 發生錯誤: {str(e)}")
    import traceback
    traceback.print_exc()
