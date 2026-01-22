import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    LINK_BR_AFILIADO = os.getenv("LINK_BR_AFILIADO")
    LINK_EN_AFILIADO = os.getenv("LINK_EN_AFILIADO")
    
    WIN_RATE = float(os.getenv("WIN_RATE", "0.75"))
    MAX_BALANCE = float(os.getenv("MAX_BALANCE", "200.0"))
    INITIAL_BONUS = float(os.getenv("INITIAL_BONUS", "50.0"))

    # Gatilhos Visuais (Imagens de alta conversão)
    IMG_MAIN = "https://i.imgur.com/8Yv6Z6H.jpeg" # Banner Cassino Luxo
    IMG_TIGER = "https://i.imgur.com/mQvXWvB.png" # Fortune Tiger
    IMG_AVIATOR = "https://i.imgur.com/uXp8V6n.jpeg" # Aviator
    IMG_ROLETA = "https://i.imgur.com/7L9R8mX.jpeg" # Roleta
    IMG_WIN = "https://i.imgur.com/2X8W8X8.jpeg" # Celebração de Vitória

settings = Settings()
