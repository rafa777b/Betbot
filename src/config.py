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

    # Gatilhos Visuais (Links diretos e globais para evitar bloqueio regional)
    # Usando links de CDN estáveis
    IMG_MAIN = "https://i.postimg.cc/m2mX8z8z/casino-main.jpg" 
    IMG_TIGER = "https://i.postimg.cc/02P0XyYy/tiger.png"
    IMG_AVIATOR = "https://i.postimg.cc/9fXfXzXz/aviator.jpg"
    IMG_ROLETA = "https://i.postimg.cc/7L9R8mX.jpeg"
    IMG_WIN = "https://i.postimg.cc/3CjE4Y9Lo4uR/win.jpg"

settings = Settings()
