import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DOCS_PATH: str = os.getenv("DOCS_PATH", "docs")

    CHROMADB_PATH: str = os.getenv("CHROMADB_PATH", "chroma_data")
    COLLECTION: str = os.getenv("COLLECTION", "docs")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "embeddinggemma")
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "384"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "40"))

    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-oss:20b-cloud")
    OLLAMA_KEY: str | None = os.getenv("OLLAMA_KEY") or None
    DB_URL: str = os.getenv("DB_URL")
    DB_ECHO: int = 1 if int(os.getenv("DB_ECHO")) == 1 else 0

    def __init__(self):
        if not self.DB_URL:
            raise ValueError("DB_URL is not set in the environment")
