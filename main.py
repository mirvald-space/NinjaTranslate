"""
Main entry point for the NinjaTranslate bot.
"""
import asyncio
import logging
from aiohttp import web, ClientSession
from bot.bot import start_bot
import os

# Создаем веб-приложение для Render
async def handle_root(request):
    return web.Response(text="NinjaTranslate bot is running!")

# Функция для предотвращения спящего режима Render
async def keep_alive(app_url):
    """
    Пингует приложение каждые 14 минут для предотвращения спящего режима на Render.
    
    Args:
        app_url: URL приложения для пинга
    """
    while True:
        try:
            async with ClientSession() as session:
                async with session.get(app_url) as response:
                    logging.info(f"Keep-alive ping sent, status: {response.status}")
        except Exception as e:
            logging.error(f"Error in keep-alive ping: {e}")
        
        # Ждем 14 минут перед следующим пингом (Render засыпает после 15 минут неактивности)
        await asyncio.sleep(840)  # 14 минут * 60 секунд

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
    
    # Получаем URL для пинга приложения (из переменной окружения или используем localhost)
    app_url = os.environ.get('APP_URL', f'http://localhost:{port}')
    
    # Запускаем задачу для предотвращения спящего режима
    asyncio.create_task(keep_alive(app_url))
    logging.info(f"Keep-alive service started, pinging {app_url}")
    
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