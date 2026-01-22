import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from src.config import settings
from src.database.db import init_db
from src.handlers import base, games, extra

# Configuração de logging agressiva para ver tudo no Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("--- INICIANDO BOT DE CASSINO ---")
    
    # Validação de segurança com log explícito
    token = settings.TELEGRAM_TOKEN
    if not token or token == "seu_token_aqui":
        logger.error("ERRO: TELEGRAM_TOKEN não configurado ou padrão!")
        return

    try:
        logger.info("Inicializando banco de dados SQLite...")
        await init_db()
        
        logger.info("Conectando ao Telegram API...")
        bot = Bot(token=token)
        
        # Testar conexão com o bot
        me = await bot.get_me()
        logger.info(f"Conectado com sucesso como: @{me.username}")
        
        dp = Dispatcher()
        
        # Registrar Routers
        dp.include_router(base.router)
        dp.include_router(games.router)
        dp.include_router(extra.router)
        
        logger.info("Iniciando Polling (Escuta de mensagens)...")
        # Skip_updates=True limpa mensagens antigas para evitar spam no reinício
        await dp.start_polling(bot, skip_updates=True)
        
    except Exception as e:
        logger.exception(f"FALHA CRÍTICA NA INICIALIZAÇÃO: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot encerrado manualmente.")
    except Exception as e:
        logger.critical(f"Erro fatal no loop principal: {e}")
