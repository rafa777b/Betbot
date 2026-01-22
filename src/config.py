import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    LINK_BR_AFILIADO: str
    LINK_EN_AFILIADO: str
    
    WIN_RATE: float = 0.75  # 75% de chance de vitória
    MAX_BALANCE: float = 200.0
    INITIAL_BONUS: float = 50.0
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
