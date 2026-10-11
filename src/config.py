"""
All settings in one place, read from environment variables (or the .env file).

In Docker, the same variables come from `--env-file .env` instead of the file on disk.
"""

from functools import lru_cache
from pathlib import Path
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()  # copies values from .env into os.environ (does nothing if .env is absent)

ROOT = Path(__file__).resolve().parent.parent  # project root folder


class Settings(BaseModel):
    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    # Max seconds to wait for one LLM call before retrying (prevents a stalled call hanging a request).
    llm_timeout_seconds: int = int(os.getenv("LLM_TIMEOUT_SECONDS", "120"))
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
    embedding_dimension: int = int(os.getenv("EMBEDDING_DIMENSION", "3072"))

    # Pinecone
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    pinecone_index_name: str = os.getenv(
        "PINECONE_INDEX_NAME", "runbook-copilot"
    )
    pinecone_namespace: str = os.getenv("PINECONE_NAMESPACE", "incident-runbooks")
    pinecone_cloud: str = os.getenv("PINECONE_CLOUD", "aws")
    pinecone_region: str = os.getenv("PINECONE_REGION", "us-east-1")

    # Internet search
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")

    # Self-RAG controls (upper limits on retry loops so a question can't loop forever)
    top_k: int = int(os.getenv("TOP_K", "5"))
    max_support_retries: int = int(os.getenv("MAX_SUPPORT_RETRIES", "2"))
    max_retrieval_rewrites: int = int(os.getenv("MAX_RETRIEVAL_REWRITES", "2"))
    max_web_rewrites: int = int(os.getenv("MAX_WEB_REWRITES", "2"))
    # SQLite audit log file (src/db.py). Relative paths are resolved from the project root.
    database_path: str = os.getenv("DATABASE_PATH", "data/audit.db")

    @property
    def database_file(self) -> Path:
        p = Path(self.database_path)
        return p if p.is_absolute() else ROOT / p


# lru_cache = build Settings once, then return the same object on every call.
@lru_cache
def get_settings() -> Settings:
    return Settings()
