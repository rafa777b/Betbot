import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from src.config import settings
from src.database.db import init_db
from src.handlers import base, games, extra

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("--- INICIANDO BOT ULTIMATE V10 (ESTABILIDADE TOTAL) ---")
    
    # Log de depuração de variáveis (sem mostrar o token inteiro por segurança)
    token = settings.TELEGRAM_TOKEN
    if token:
        logger.info(f"Token configurado: {token[:5]}...{token[-5:]}")
    else:
        logger.error("TELEGRAM_TOKEN NÃO ENCONTRADO!")
        return

    try:
        # 1. Inicializar Banco
        await init_db()
        logger.info("Banco de dados SQLite inicializado.")
        
        # 2. Configurar Bot (Compatível com aiogram 3.4.1)
        bot = Bot(token=token)
        
        # 3. Limpeza de Webhook
        logger.info("Limpando Webhooks e mensagens pendentes...")
        await bot.delete_webhook(drop_pending_updates=True)
        
        # 4. Teste de Identidade
        me = await bot.get_me()
        logger.info(f"BOT ONLINE: @{me.username}")
        
        # 5. Configurar Dispatcher
        dp = Dispatcher()
        dp.include_router(base.router)
        dp.include_router(games.router)
        dp.include_router(extra.router)
        
        logger.info("Iniciando Polling... O bot deve responder agora!")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.exception(f"FALHA CRÍTICA: {e}")
        await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot encerrado.")
    except Exception as e:
        logger.critical(f"ERRO FATAL: {e}")
        sys.exit(1)
