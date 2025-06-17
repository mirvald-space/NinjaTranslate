"""
Main entry point for the NinjaTranslate bot.
"""
import asyncio
import logging
from aiohttp import web, ClientSession
from bot.bot import start_bot
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
    # Start the bot
    asyncio.create_task(start_bot())
    
    # Create web application
    app = web.Application()
    app.router.add_get('/', handle_root)
    
    # Configure port (Render requires using PORT environment variable)
    port = int(os.environ.get('PORT', 8080))
    
    # Start the server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    logging.info(f"Web server started on port {port}")
    
    # Get URL for pinging the application (from environment variable or use localhost)
    app_url = os.environ.get('APP_URL', f'http://localhost:{port}')
    
    # Start task to prevent sleep mode
    asyncio.create_task(keep_alive(app_url))
    logging.info(f"Keep-alive service started, pinging {app_url}")
    
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