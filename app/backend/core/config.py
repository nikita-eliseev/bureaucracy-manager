from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "dev"
    debug: bool = False
    
    database_url: str = Field(validation_alias="DATABASE_URL")
    
    algorithm: str
    secret_key: str
    
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    
    model_config = SettingsConfigDict(
        env_file=".env",   
        case_sensitive=False
    )
    
    
settings = Settings()