import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
COMPANY_DOCS_DIR = BASE_DIR / "data" / "company_docs"
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"
COMPANY_COLLECTION = "company_kb"

# --- LLM ---
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

# --- Embeddings (free, runs locally) ---
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# --- Chunking & retrieval ---
CHUNK_SIZE = 1000      # characters
CHUNK_OVERLAP = 150
TOP_K = 4

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md", ".log", ".json", ".csv", ".py"}

# --- Login & admin ---
DB_PATH = BASE_DIR / "data" / "users.db"
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")   # change this in .env
ALLOW_SIGNUP = os.getenv("ALLOW_SIGNUP", "true").lower() == "true"
