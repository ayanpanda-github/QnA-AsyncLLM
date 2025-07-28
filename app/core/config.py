from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://user:password@localhost/docqa"
    llm_delay: int = 5
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
