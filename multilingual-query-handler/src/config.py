import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")

# Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.3-70b-versatile"

# Vector DB Settings
VECTOR_DB_TYPE = "chroma"  # or "faiss"
COLLECTION_NAME = "customer_support_docs"

# Chunking Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Paths
DATA_DIR = "data"
RAW_DATA_DIR = f"{DATA_DIR}/raw"
PROCESSED_DATA_DIR = f"{DATA_DIR}/processed"