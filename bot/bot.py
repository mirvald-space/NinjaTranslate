"""
Main bot module for the NinjaTranslate bot.
"""
import logging
from aiogram import Bot, Dispatcher
from config import config
from bot.handlers import router
from bot.db import init_db

async def start_bot():
    """
    Initialize and start the bot.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Validate configuration
    if not config.validate_tokens():
        logging.error("Invalid configuration: Missing BOT_TOKEN or XAI_API_KEY")
        return
    
    # Initialize database
    await init_db()
    
    # Initialize bot and dispatcher
    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    
    # Include routers
    dp.include_router(router)
    
    # Start polling
    logging.info("Starting NinjaTranslate bot")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot) 