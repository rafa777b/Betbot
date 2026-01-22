import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from src.config import settings
from src.database.db import init_db
from src.handlers import base, games, extra

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    # Validação de segurança
    if not settings.TELEGRAM_TOKEN:
        logger.error("ERRO CRÍTICO: TELEGRAM_TOKEN não configurado!")
        logger.error("Certifique-se de configurar as variáveis de ambiente no painel da Railway.")
        sys.exit(1)

    logger.info("Iniciando inicialização do banco de dados...")
    await init_db()
    
    logger.info("Configurando Bot e Dispatcher...")
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    dp = Dispatcher()
    
    # Registrar Routers
    dp.include_router(base.router)
    dp.include_router(games.router)
    dp.include_router(extra.router)
    
    logger.info("Bot de Cassino iniciado com sucesso! Aguardando mensagens...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot parado pelo usuário ou sistema.")
    except Exception as e:
        logger.exception(f"Ocorreu um erro inesperado: {e}")
        sys.exit(1)
