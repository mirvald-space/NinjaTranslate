# NinjaTranslate

![NinjaTranslate Cover](cover.png)

A Telegram translator bot that uses X.AI API to translate between any languages.

**README Languages**
- 🇬🇧 [English](README.md) (current)
- 🇺🇦 [Українська](README_uk.md)
- 🇷🇺 [Русский](README_ru.md)

## Features

- Universal translation between 18+ languages
- Flag emojis for easy language identification
- Two-step language selection flow (source and target)
- Easy language selection via inline buttons
- Handles up to 2000 characters per request
- Error handling for API failures
- Multilingual user interface (Arabic/English)
- MongoDB integration for user data storage
- Admin statistics
- Webhook support for cloud deployment
- Auto-ping to prevent idle state on free hosting plans
- Subscription requirement system (users must subscribe to specified channels to use the bot)

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
   CHANNEL_ID_1=@your_first_channel
   CHANNEL_ID_2=@your_second_channel
   ADMIN_IDS=123456789,987654321
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
   CHANNEL_ID_1=@your_first_channel
   CHANNEL_ID_2=@your_second_channel
   ADMIN_IDS=123456789,987654321
   ```
5. Deploy the service

The bot will automatically use webhook mode when deployed to Render and includes a built-in keep-alive mechanism to prevent the service from going to sleep on free plans.

## Usage

1. Start a chat with your bot on Telegram
2. Subscribe to the required channels
3. Verify your subscription when prompted
4. Send `/start` to begin translation
5. Select the source language
6. Select the target language
7. Send any text (up to 2000 characters) to translate

## Bot Commands

- `/start` - Start the bot and display source language selection
- `/translate` or `/tr` - Start a new translation
- `/language` or `/lang` - Change the interface language (Arabic/English)
- `/stats` - View bot usage statistics (admin only)

## Subscription System

The bot requires users to be subscribed to specified channels to use its translation functions:

- Set the channel usernames/IDs in your environment variables (`CHANNEL_ID_1` and `CHANNEL_ID_2`)
- Users will be prompted to subscribe when they first use the bot
- After subscribing, they can click the "Check Subscription" button
- The bot periodically re-checks subscription status (configurable interval)
- Admin users (specified by `ADMIN_IDS`) bypass the subscription requirement

## Database Structure

User collection:
```
{
  "user_id": 123456789,          // Telegram user ID
  "username": "username",         // Telegram username
  "first_name": "First",          // User's first name
  "last_name": "Last",            // User's last name
  "ui_lang": "en",                // Interface language (en/ar)
  "last_activity": ISODate(...),  // Last activity timestamp
  "subscription_verified": true,  // Whether user has verified subscriptions
  "subscription_last_checked": ISODate(...) // When subscription was last checked
}
```

## Supported Languages

- 🇬🇧 English
- 🇸🇦 Arabic
- 🇪🇸 Spanish
- 🇫🇷 French
- 🇩🇪 German
- 🇨🇳 Chinese
- 🇷🇺 Russian
- 🇵🇹 Portuguese
- 🇯🇵 Japanese
- 🇮🇹 Italian
- 🇰🇷 Korean
- 🇹🇷 Turkish
- 🇳🇱 Dutch
- 🇸🇪 Swedish
- 🇵🇱 Polish
- 🇻🇳 Vietnamese
- 🇮🇳 Hindi
- 🇺🇦 Ukrainian

More languages can be easily added by extending the `LANGUAGES` dictionary in `translations.py`. 