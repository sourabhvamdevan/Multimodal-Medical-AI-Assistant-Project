

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Multimodal Medical AI Gateway"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SQLITE_DB_FILE: str = "medical_assistant.db"
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    
    GROQ_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""
    
    SECRET_KEY: str = "SUPER_SECRET_CLINICAL_GATEWAY_KEY_CHANGE_IN_PRODUCTION"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()