# NinjaTranslate

A Telegram translator bot that uses X.AI API to translate between Arabic and English.

## Features

- Translations between Arabic and English
- Easy language selection via inline buttons
- Handles up to 2000 characters per request
- Error handling for API failures
- Multilingual user interface (Arabic/English)
- MongoDB integration for user data storage
- Admin statistics
- Webhook support for cloud deployment
- Auto-ping to prevent idle state on free hosting plans

## Project Structure

```
NinjaTranslate/
├── bot/
│   ├── __init__.py
│   ├── bot.py           # Main bot module
│   ├── db.py            # Database operations
│   ├── handlers.py      # Message handlers
│   ├── keyboards.py     # Telegram keyboards
│   ├── localization.py  # UI translations
│   └── translations.py  # Translation service
├── config.py            # Configuration
├── main.py              # Entry point with webhook support
├── .env-example         # Example env file
├── requirements.txt     # Dependencies
└── README.md            # This file
```

## Setup

### Local Development

1. Clone this repository
2. Create a `.env` file with your tokens (see `.env-example` for reference)
   ```
   BOT_TOKEN=your_telegram_bot_token_here
   XAI_API_KEY=your_xai_api_key_here
   MONGO_URI=mongodb://localhost:27017
   MONGO_DB=ninja_translate_bot
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```
   python main.py
   ```

### Deploying to Render

1. Create a new Web Service in Render dashboard
2. Connect to your GitHub repository
3. Configure the following settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
4. Add the following environment variables:
   ```
   BOT_TOKEN=your_telegram_bot_token_here
   XAI_API_KEY=your_xai_api_key_here
   MONGO_URI=your_mongodb_connection_string
   MONGO_DB=ninja_translate_bot
   APP_URL=https://your-app-name.onrender.com
   ```
5. Deploy the service

The bot will automatically use webhook mode when deployed to Render and includes a built-in keep-alive mechanism to prevent the service from going to sleep on free plans.

## Usage

1. Start a chat with your bot on Telegram
2. Send `/start` to get language selection buttons
3. Select a translation direction
4. Send any text (up to 2000 characters) to translate

## Bot Commands

- `/start` - Start the bot and display language selection
- `/language` or `/lang` - Change the interface language (Arabic/English)
- `/stats` - View bot usage statistics (admin only)

## Database Structure

User collection:
```
{
  "user_id": 123456789,          // Telegram user ID
  "username": "username",         // Telegram username
  "first_name": "First",          // User's first name
  "last_name": "Last",            // User's last name
  "ui_lang": "en",                // Interface language (en/ar)
  "last_activity": ISODate(...)   // Last activity timestamp
}
```

## Supported Translation Directions

- Arabic → English
- English → Arabic 