import os
from dotenv import load_dotenv

load_dotenv()  # carga .env desde CWD o directorios padre

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")
API_PORT = int(os.getenv("API_PORT", "5000"))
