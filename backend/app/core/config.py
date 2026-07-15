"""Application configuration using Pydantic BaseSettings."""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise Multimodal Chatbot"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str = "gpt-5.5"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/chatbot"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Azure Storage
    AZURE_STORAGE_CONNECTION_STRING: str

    # LangSmith
    LANGSMITH_API_KEY: Optional[str] = None
    LANGSMITH_PROJECT: str = "enterprise-chatbot"
    LANGSMITH_TRACING: bool = True
    LANGCHAIN_TRACING_V2: bool = True

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()