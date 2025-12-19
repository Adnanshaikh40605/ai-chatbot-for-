from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Available models:")
print("-" * 50)

try:
    for model in client.models.list():
        print(f"Name: {model.name}")
        print(f"Display Name: {model.display_name}")
        print("-" * 50)
except Exception as e:
    print(f"Error listing models: {e}")
