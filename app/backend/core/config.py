from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "dev"
    debug: bool = "False"
    
    database_url: str
    
    model_config = SettingsConfigDict(
        env_file=".env",     #    return later
        case_sensitive=False
    )
    
    
setting = Settings()