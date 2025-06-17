"""
Main entry point for the NinjaTranslate bot.
"""
import asyncio
import logging
from aiohttp import web
from bot.bot import start_bot
import os

# Создаем веб-приложение для Render
async def handle_root(request):
    return web.Response(text="NinjaTranslate bot is running!")

async def setup_server():
    # Запуск бота
    asyncio.create_task(start_bot())
    
    # Создаем веб-приложение
    app = web.Application()
    app.router.add_get('/', handle_root)
    
    # Настраиваем порт (Render требует использовать переменную окружения PORT)
    port = int(os.environ.get('PORT', 8080))
    
    # Запускаем сервер
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    logging.info(f"Web server started on port {port}")
    
    # Ждем бесконечно
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(setup_server())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Bot stopped due to error: {e}", exc_info=True) 