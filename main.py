"""
Main entry point for the NinjaTranslate bot.
"""
import asyncio
import logging
from bot.bot import start_bot

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Bot stopped due to error: {e}", exc_info=True) 