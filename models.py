import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Ensure your API key is set
# os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY", ""))

print("List of available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)