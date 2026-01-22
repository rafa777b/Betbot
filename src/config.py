import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Prioriza variáveis de ambiente do sistema (Railway), depois o .env
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    LINK_BR_AFILIADO = os.getenv("LINK_BR_AFILIADO")
    LINK_EN_AFILIADO = os.getenv("LINK_EN_AFILIADO")
    
    WIN_RATE = float(os.getenv("WIN_RATE", "0.75"))
    MAX_BALANCE = float(os.getenv("MAX_BALANCE", "200.0"))
    INITIAL_BONUS = float(os.getenv("INITIAL_BONUS", "50.0"))

settings = Settings()
