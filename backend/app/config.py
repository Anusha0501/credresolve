import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    DATABASE_URL = "sqlite:///./credresolve.db"
    CHROMA_PERSIST_DIR = "./chroma_db"
    
config = Config()
