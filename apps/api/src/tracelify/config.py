"""Configuration and settings for Tracelify."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CHROMA_DIR = PROJECT_ROOT / "chroma_data"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
CHROMA_DIR.mkdir(exist_ok=True)

# Chunking settings
CHUNK_SIZE = 500  # Target tokens per chunk
CHUNK_OVERLAP = 50  # Overlap tokens between chunks

# Retrieval settings
TOP_K = 3  # Number of chunks to retrieve

# Model settings
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "deepseek-chat"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
