"""
Main entry point for the NinjaTranslate bot.
"""
import asyncio
import logging
from aiohttp import web, ClientSession
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from bot.handlers import router
from bot.db import init_db
from config import config
import os

# Create web application for Render
async def handle_root(request):
    return web.Response(text="NinjaTranslate bot is running!")

# Function to prevent Render from sleeping
async def keep_alive(app_url):
    """
    Pings the application every 14 minutes to prevent sleep mode on Render.
    
    Args:
        app_url: Application URL to ping
    """
    while True:
        try:
            async with ClientSession() as session:
                async with session.get(app_url) as response:
                    logging.info(f"Keep-alive ping sent, status: {response.status}")
        except Exception as e:
            logging.error(f"Error in keep-alive ping: {e}")
        
        # Wait 14 minutes before next ping (Render sleeps after 15 minutes of inactivity)
        await asyncio.sleep(840)  # 14 minutes * 60 seconds

async def setup_server():
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
    
    # Configure port and URLs
    port = int(os.environ.get('PORT', 8080))
    base_url = os.environ.get('APP_URL', f'http://localhost:{port}')
    webhook_path = "/webhook"
    webhook_url = f"{base_url}{webhook_path}"
    
    # Initialize bot and dispatcher with webhook mode
    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    
    # Include routers
    dp.include_router(router)
    
    # Create web application
    app = web.Application()
    
    # Add main route
    app.router.add_get('/', handle_root)
    
    # Setup webhook handling
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    ).register(app, path=webhook_path)
    
    # Setup application
    setup_application(app, dp, bot=bot)
    
    # Set webhook
    await bot.set_webhook(url=webhook_url)
    logging.info(f"Webhook set to URL: {webhook_url}")
    
    # Start the server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    logging.info(f"Web server started on port {port}")
    
    # Start keep-alive task
    asyncio.create_task(keep_alive(base_url))
    logging.info(f"Keep-alive service started, pinging {base_url}")
    
    # Wait indefinitely
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(setup_server())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Bot stopped due to error: {e}", exc_info=True) 