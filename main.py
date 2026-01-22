import asyncio
import logging
from aiogram import Bot, Dispatcher
from src.config import settings
from src.database.db import init_db
from src.handlers import base, games, extra

# Configuração de logging
logging.basicConfig(level=logging.INFO)

async def main():
    # Inicializar Banco de Dados
    await init_db()
    
    # Inicializar Bot e Dispatcher
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    dp = Dispatcher()
    
    # Registrar Routers
    dp.include_router(base.router)
    dp.include_router(games.router)
    dp.include_router(extra.router)
    
    # Iniciar Polling
    logging.info("Bot de Cassino iniciado com sucesso!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot parado.")
