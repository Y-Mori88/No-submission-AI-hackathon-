from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "local"
    allow_origins: str = "http://localhost:3000"

    gcp_project: str = ""
    gcp_region: str = "asia-northeast1"
    gemini_model: str = "gemini-1.5-pro"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
