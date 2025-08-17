# 🐪 NinjaTranslate

![NinjaTranslate Cover](cover.png)

<div align="center">

### 🌍 Choose Your Language | Выберите язык | Оберіть мову

[![English](https://img.shields.io/badge/🇬🇧_English-blue?style=for-the-badge)](#english-🇬🇧) 
[![Русский](https://img.shields.io/badge/🇷🇺_Русский-red?style=for-the-badge)](#русский-🇷🇺) 
[![Українська](https://img.shields.io/badge/🇺🇦_Українська-yellow?style=for-the-badge)](#українська-🇺🇦)

</div>

---

## English 🇬🇧

A Telegram translator bot that uses X.AI API to translate between any languages.

### ✨ Features

- 🌐 Universal translation between 18+ languages
- 🏳️ Flag emojis for easy language identification
- 🔄 Two-step language selection flow (source and target)
- 🎛️ Easy language selection via inline buttons
- 📝 Handles up to 2000 characters per request
- ⚡ Error handling for API failures
- 🌍 Multilingual user interface (Arabic/English)
- 🗄️ MongoDB integration for user data storage
- 📊 Admin statistics
- 🔐 Subscription requirement system

### 📁 Project Structure

```
NinjaTranslate/
├── bot/
│   ├── __init__.py
│   ├── bot.py           # Main bot module with polling
│   ├── db.py            # Database operations
│   ├── handlers.py      # Message handlers
│   ├── keyboards.py     # Telegram keyboards
│   ├── localization.py  # UI translations
│   └── translations.py  # Translation service
├── config.py            # Configuration
├── main.py              # Entry point (polling mode)
├── .env-example         # Example env file
├── requirements.txt     # Dependencies
└── README.md            # This file
```

### 🚀 Setup

#### Local Development

1. Clone this repository
2. Create a `.env` file with your tokens:
   ```env
   BOT_TOKEN=your_telegram_bot_token_here
   XAI_API_KEY=your_xai_api_key_here
   MONGO_URI=mongodb://localhost:27017
   MONGO_DB=ninja_translate_bot
   CHANNEL_ID_1=@your_first_channel
   CHANNEL_ID_2=@your_second_channel
   ADMIN_IDS=123456789,987654321
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

### 🎯 Usage

1. Start a chat with your bot on Telegram
2. Subscribe to the required channels
3. Send `/start` to begin translation
4. Select the source language
5. Select the target language  
6. Send any text (up to 2000 characters) to translate

### 🤖 Bot Commands

- `/start` - Start the bot and display source language selection
- `/translate` or `/tr` - Start a new translation
- `/language` or `/lang` - Change the interface language
- `/stats` - View bot usage statistics (admin only)

### 🌍 Supported Languages

🇬🇧 English • 🇸🇦 Arabic • 🇪🇸 Spanish • 🇫🇷 French • 🇩🇪 German • 🇨🇳 Chinese • 🇷🇺 Russian • 🇵🇹 Portuguese • 🇯🇵 Japanese • 🇮🇹 Italian • 🇰🇷 Korean • 🇹🇷 Turkish • 🇳🇱 Dutch • 🇸🇪 Swedish • 🇵🇱 Polish • 🇻🇳 Vietnamese • 🇮🇳 Hindi • 🇺🇦 Ukrainian

---

## Русский 🇷🇺

Телеграм-бот для перевода, использующий API X.AI для перевода между любыми языками.

### ✨ Особенности

- 🌐 Универсальный перевод между 18+ языками
- 🏳️ Эмодзи с флагами для легкой идентификации языков
- 🔄 Двухэтапный процесс выбора языка (исходный и целевой)
- 🎛️ Простой выбор языков через встроенные кнопки
- 📝 Обрабатывает до 2000 символов за запрос
- ⚡ Обработка ошибок API
- 🌍 Многоязычный пользовательский интерфейс
- 🗄️ Интеграция с MongoDB для хранения данных
- 📊 Статистика для администраторов
- 🔐 Система обязательной подписки

### 📁 Структура проекта

```
NinjaTranslate/
├── bot/
│   ├── __init__.py
│   ├── bot.py           # Главный модуль бота (polling режим)
│   ├── db.py            # Операции с базой данных
│   ├── handlers.py      # Обработчики сообщений
│   ├── keyboards.py     # Клавиатуры Telegram
│   ├── localization.py  # Переводы интерфейса
│   └── translations.py  # Сервис перевода
├── config.py            # Конфигурация
├── main.py              # Точка входа (polling режим)
├── .env-example         # Пример env-файла
├── requirements.txt     # Зависимости
└── README.md            # Этот файл
```

### 🚀 Настройка

#### Локальная разработка

1. Клонируйте этот репозиторий
2. Создайте файл `.env` с вашими токенами:
   ```env
   BOT_TOKEN=your_telegram_bot_token_here
   XAI_API_KEY=your_xai_api_key_here
   MONGO_URI=mongodb://localhost:27017
   MONGO_DB=ninja_translate_bot
   CHANNEL_ID_1=@your_first_channel
   CHANNEL_ID_2=@your_second_channel
   ADMIN_IDS=123456789,987654321
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Запустите бота:
   ```bash
   python main.py
   ```

### 🎯 Использование

1. Начните чат с вашим ботом в Telegram
2. Подпишитесь на требуемые каналы
3. Отправьте `/start`, чтобы начать перевод
4. Выберите исходный язык
5. Выберите целевой язык
6. Отправьте любой текст (до 2000 символов) для перевода

### 🤖 Команды бота

- `/start` - Запустить бота и отобразить выбор исходного языка
- `/translate` или `/tr` - Начать новый перевод
- `/language` или `/lang` - Изменить язык интерфейса
- `/stats` - Просмотреть статистику (только для администраторов)

### 🌍 Поддерживаемые языки

🇬🇧 Английский • 🇸🇦 Арабский • 🇪🇸 Испанский • 🇫🇷 Французский • 🇩🇪 Немецкий • 🇨🇳 Китайский • 🇷🇺 Русский • 🇵🇹 Португальский • 🇯🇵 Японский • 🇮🇹 Итальянский • 🇰🇷 Корейский • 🇹🇷 Турецкий • 🇳🇱 Нидерландский • 🇸🇪 Шведский • 🇵🇱 Польский • 🇻🇳 Вьетнамский • 🇮🇳 Хинди • 🇺🇦 Украинский

---

## Українська 🇺🇦

Телеграм-бот для перекладу, що використовує API X.AI для перекладу між будь-якими мовами.

### ✨ Особливості

- 🌐 Universal переклад між 18+ мовами
- 🏳️ Емодзі з прапорами для легкої ідентифікації мов
- 🔄 Двоетапний процес вибору мови (вихідна та цільова)
- 🎛️ Простий вибір мов через вбудовані кнопки
- 📝 Обробляє до 2000 символів за запит
- ⚡ Обробка помилок API
- 🌍 Багатомовний інтерфейс користувача
- 🗄️ Інтеграція з MongoDB для зберігання даних
- 📊 Статистика для адміністраторів
- 🔐 Система обов'язкової підписки

### 📁 Структура проекту

```
NinjaTranslate/
├── bot/
│   ├── __init__.py
│   ├── bot.py           # Головний модуль бота (polling режим)
│   ├── db.py            # Операції з базою даних
│   ├── handlers.py      # Обробники повідомлень
│   ├── keyboards.py     # Клавіатури Telegram
│   ├── localization.py  # Переклади інтерфейсу
│   └── translations.py  # Сервіс перекладу
├── config.py            # Конфігурація
├── main.py              # Точка входу (polling режим)
├── .env-example         # Приклад env-файлу
├── requirements.txt     # Залежності
└── README.md            # Цей файл
```

### 🚀 Налаштування

#### Локальна розробка

1. Клонуйте цей репозиторій
2. Створіть файл `.env` з вашими токенами:
   ```env
   BOT_TOKEN=your_telegram_bot_token_here
   XAI_API_KEY=your_xai_api_key_here
   MONGO_URI=mongodb://localhost:27017
   MONGO_DB=ninja_translate_bot
   CHANNEL_ID_1=@your_first_channel
   CHANNEL_ID_2=@your_second_channel
   ADMIN_IDS=123456789,987654321
   ```
3. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```
4. Запустіть бота:
   ```bash
   python main.py
   ```

### 🎯 Використання

1. Почніть чат зі своїм ботом у Telegram
2. Підпишіться на необхідні канали
3. Надішліть `/start`, щоб почати переклад
4. Виберіть вихідну мову
5. Виберіть цільову мову
6. Надішліть будь-який текст (до 2000 символів) для перекладу

### 🤖 Команди бота

- `/start` - Запустити бота та відобразити вибір вихідної мови
- `/translate` або `/tr` - Почати новий переклад
- `/language` або `/lang` - Змінити мову інтерфейсу
- `/stats` - Переглянути статистику (тільки для адміністраторів)

### 🌍 Підтримувані мови

🇬🇧 Англійська • 🇸🇦 Арабська • 🇪🇸 Іспанська • 🇫🇷 Французька • 🇩🇪 Німецька • 🇨🇳 Китайська • 🇷🇺 Російська • 🇵🇹 Португальська • 🇯🇵 Японська • 🇮🇹 Італійська • 🇰🇷 Корейська • 🇹🇷 Турецька • 🇳🇱 Нідерландська • 🇸🇪 Шведська • 🇵🇱 Польська • 🇻🇳 В'єтнамська • 🇮🇳 Хінді • 🇺🇦 Українська

---

<div align="center">

### 🛠️ Database Structure

```json
{
  "user_id": 123456789,
  "username": "username",
  "first_name": "First",
  "last_name": "Last", 
  "ui_lang": "en",
  "last_activity": "ISODate(...)",
  "subscription_verified": true,
  "subscription_last_checked": "ISODate(...)"
}
```

**Made with ❤️ for polyglots worldwide**

</div>