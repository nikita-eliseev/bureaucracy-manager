from datetime import date
from dateutil.relativedelta import relativedelta
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "dev"
    debug: bool = False
    
    database_url: str = Field(validation_alias="DATABASE_URL")
    
    cors_origins: str = ""
    
    algorithm: str
    
    secret_key: str
    
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    
    model_config = SettingsConfigDict(
        env_file=".env",   
        case_sensitive=False
    )
    
    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]
    
    
settings = Settings()

def calculate_cancellation_deadline(
    end_date: date,
    notice_period_months: int
) -> date:
    return end_date - relativedelta(months=notice_period_months)