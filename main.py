import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from src.config import settings
from src.database.db import init_db
from src.handlers import base, games, extra

# Configuração de logging otimizada para Cloud
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("--- INICIANDO BOT ULTIMATE V8 (ESTABILIDADE GLOBAL) ---")
    
    if not settings.TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN ausente!")
        return

    try:
        await init_db()
        
        # Configurações de bot para evitar timeouts
        bot = Bot(
            token=settings.TELEGRAM_TOKEN,
            default=DefaultBotProperties(parse_mode='HTML')
        )
        
        dp = Dispatcher()
        dp.include_router(base.router)
        dp.include_router(games.router)
        dp.include_router(extra.router)
        
        # Teste de conexão
        me = await bot.get_me()
        logger.info(f"Bot @{me.username} online e operando!")

        # Polling otimizado: 
        # skip_updates=True evita processar lixo acumulado
        # close_bot_session=True garante limpeza ao fechar
        await dp.start_polling(bot, skip_updates=True)
        
    except Exception as e:
        logger.exception(f"Erro na execução: {e}")
        # Pequeno delay antes de tentar novamente (o Railway reiniciará o processo)
        await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Encerrado.")
    except Exception as e:
        logger.critical(f"Erro fatal: {e}")
        sys.exit(1)
