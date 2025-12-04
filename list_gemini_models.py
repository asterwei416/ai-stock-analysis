"""
測試 Gemini API 並列出所有可用模型
使用方法: python list_gemini_models.py YOUR_API_KEY
"""
import google.generativeai as genai
import sys

print("=" * 60)
print("Gemini API 模型測試")
print("=" * 60)
print(f"google-generativeai 版本: {genai.__version__ if hasattr(genai, '__version__') else '未知'}")
print()

# 從命令行參數獲取 API Key
if len(sys.argv) < 2:
    print("⚠️  請提供您的 Gemini API Key")
    print()
    print("使用方法:")
    print("  python list_gemini_models.py YOUR_API_KEY")
    print()
    print("或者從主應用獲取(如果您已經在 Streamlit 應用中輸入過):")
    print("  從側邊欄複製您的 Gemini API Key")
    print()
    input("按 Enter 鍵退出...")
    sys.exit(1)

API_KEY = sys.argv[1]

try:
    # 配置 API
    genai.configure(api_key=API_KEY)
    
    print("正在列出所有可用模型...")
    print("-" * 60)
    
    # 列出所有模型
    models = list(genai.list_models())
    
    if not models:
        print("⚠️  未找到任何模型")
        print()
        print("可能的原因:")
        print("  1. API Key 無效")
        print("  2. 網路連線問題")
        print("  3. API 服務暫時不可用")
        input("按 Enter 鍵退出...")
        sys.exit(1)
    
    print(f"\n找到 {len(models)} 個模型:\n")
    
    # 顯示所有模型詳情
    compatible_models = []
    for model in models:
        # 檢查是否支持 generateContent
        supports_generate = 'generateContent' in model.supported_generation_methods
        
        print(f"📦 模型名稱: {model.name}")
        print(f"   顯示名稱: {model.display_name}")
        print(f"   支持的方法: {', '.join(model.supported_generation_methods)}")
        print(f"   支持 generateContent: {'✅ 是' if supports_generate else '❌ 否'}")
        
        if supports_generate:
            compatible_models.append(model.name)
        
        print()
    
    print("=" * 60)
    print("✅ 可用於 AI 股票分析的模型:")
    print("-" * 60)
    
    if compatible_models:
        for i, model_name in enumerate(compatible_models, 1):
            # 移除 "models/" 前綴以便使用
            clean_name = model_name.replace("models/", "")
            print(f"  {i}. {clean_name}")
            
        print()
        print("=" * 60)
        print("💡 建議:")
        print("-" * 60)
        
        # 推薦最佳模型
        recommended = None
        for model_name in compatible_models:
            clean = model_name.replace("models/", "")
            if "1.5-flash" in clean:
                recommended = clean
                break
            elif "1.5-pro" in clean:
                recommended = clean
            elif "pro" in clean.lower() and not recommended:
                recommended = clean
        
        if recommended:
            print(f"  推薦使用: {recommended}")
            print(f"  (平衡性能與配額)")
        else:
            print(f"  推薦使用: {compatible_models[0].replace('models/', '')}")
        
        print()
        print("若要在主應用中使用,請將模型名稱更新到")
        print("stock_analysis_app.py 第 222 行")
    else:
        print("  ⚠️  未找到支持 generateContent 的模型")
        print()
        print("  這可能表示:")
        print("    - API Key 權限不足")
        print("    - 需要升級 API 訂閱")
    
except Exception as e:
    print(f"❌ 錯誤: {str(e)}")
    print()
    print("可能的原因:")
    print("  - API Key 無效或已過期")
    print("  - 網路連線問題")
    print("  - API 配額已用盡")
    print()
    import traceback
    traceback.print_exc()

print()
input("按 Enter 鍵退出...")
