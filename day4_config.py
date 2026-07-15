from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")
print(api_key)
if api_key is None:
    print("ERROR: API_KEY not found — check your .env file")
else:
    print("API key loaded successfully")
    