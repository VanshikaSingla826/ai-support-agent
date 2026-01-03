import google.generativeai as genai

# PASTE YOUR KEY HERE
API_KEY = "AIzaSyC2U-6yzvH_gNvULFXrGUHZ866bTG9VW2k" 

genai.configure(api_key=API_KEY)

print("Attempting to list available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")