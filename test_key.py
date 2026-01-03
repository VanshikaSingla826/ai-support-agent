import google.generativeai as genai

# Paste your key inside the quotes below
API_KEY = "AIzaSyC2U-6yzvH_gNvULFXrGUHZ866bTG9VW2k"

print(f"Testing Key: {API_KEY[:10]}...")

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say 'Hello' if this works.")
    print("\n✅ SUCCESS! The API Key is working.")
    print(f"Response: {response.text}")
except Exception as e:
    print("\n❌ FAILURE. The API Key is rejected.")
    print(f"Error Details: {e}")