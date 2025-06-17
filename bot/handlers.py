"""
Handlers module for the NinjaTranslate bot.
"""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
import os
from datetime import datetime, timedelta
from bot.keyboards import (
    get_language_keyboard, 
    get_ui_language_keyboard, 
    get_target_language_keyboard,
    get_subscription_keyboard
)
from bot.localization import get_message, localize_language_names
from bot.translations import LANGUAGES, translate_text
from bot.db import (
    save_user, 
    get_user, 
    update_user_language, 
    update_subscription_status,
    get_stats
)
from config import config

# Initialize router
router = Router()

# User states dictionary (for translation direction)
user_states = {}

# Admin user IDs
ADMIN_IDS = os.getenv("ADMIN_IDS", "").split(",")  # Replace with your actual admin ID(s)

async def check_user_subscription(bot, user_id: int):
    """
    Check if user is subscribed to all required channels.
    
    Args:
        bot: Telegram Bot instance
        user_id: Telegram user ID
        
    Returns:
        True if subscribed to all required channels, False otherwise
    """
    if not config.validate_channels():
        # If no channels are configured, assume subscription is verified
        return True
    
    for channel in config.required_channels:
        try:
            chat_member = await bot.get_chat_member(channel, user_id)
            status = chat_member.status
            if status not in ['member', 'administrator', 'creator']:
                return False
        except Exception as e:
            logging.error(f"Error checking subscription status: {e}")
            return False
    
    return True

async def check_subscription_middleware(handler, message, data):
    """
    Middleware to check user subscription before handling messages.
    
    Args:
        handler: Next handler in the chain
        message: Telegram message object
        data: Additional data
        
    Returns:
        Result of the next handler or None if subscription check fails
    """
    user_id = message.from_user.id
    bot = data["bot"]
    
    # Skip check for admin users
    if str(user_id) in ADMIN_IDS:
        return await handler(message, data)
    
    # Get user from database
    user_data = await get_user(user_id)
    ui_lang = user_data["ui_lang"] if user_data and "ui_lang" in user_data else "en"
    
    # Check if user has verified subscription or if we need to recheck
    if user_data and "subscription_verified" in user_data and user_data["subscription_verified"]:
        # Check if we need to reverify subscription (every X minutes)
        last_checked = user_data.get("subscription_last_checked")
        
        if last_checked and datetime.now() - last_checked < timedelta(minutes=config.subscription_check_interval):
            return await handler(message, data)
    
    # Check if user is subscribed to required channels
    is_subscribed = await check_user_subscription(bot, user_id)
    
    if is_subscribed:
        # Update user's subscription status
        await update_subscription_status(user_id, True)
        return await handler(message, data)
    else:
        # Update user's subscription status
        await update_subscription_status(user_id, False)
        
        # Create channel links list
        channel_links = ""
        for channel in config.required_channels:
            # Extract channel username/ID for display
            if channel.startswith('@'):
                channel_name = channel
                channel_link = f"https://t.me/{channel[1:]}"
            else:
                try:
                    chat = await bot.get_chat(channel)
                    channel_name = chat.title or channel
                    if chat.username:
                        channel_link = f"https://t.me/{chat.username}"
                    else:
                        channel_link = f"Channel ID: {channel}"
                except Exception as e:
                    logging.error(f"Error getting channel info: {e}")
                    channel_name = channel
                    channel_link = f"Channel ID: {channel}"
            
            channel_links += f"• <a href='{channel_link}'>{channel_name}</a>\n"
        
        # Send subscription required message
        await message.answer(
            get_message(ui_lang, "subscription_required", channel_links=channel_links),
            reply_markup=get_subscription_keyboard(ui_lang),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        return None

@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Handle the /start command.
    
    Args:
        message: Telegram message object
    """
    # Get user data
    user_id = message.from_user.id
    username = message.from_user.username or ""
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    
    # Default to English for new users
    ui_lang = "en"
    
    # Save user to database
    await save_user(user_id, username, first_name, last_name, ui_lang)
    
    # Check subscription
    result = await check_subscription_middleware(
        lambda msg, _: msg.answer(
            get_message(ui_lang, "welcome"),
            reply_markup=get_language_keyboard()
        ),
        message,
        {"bot": message.bot}
    )

@router.message(Command("language", "lang"))
async def cmd_language(message: Message):
    """
    Handle the /language command.
    
    Args:
        message: Telegram message object
    """
    user_id = message.from_user.id
    
    # Get user from database
    user_data = await get_user(user_id)
    ui_lang = user_data["ui_lang"] if user_data and "ui_lang" in user_data else "en"
    
    # Check subscription
    await check_subscription_middleware(
        lambda msg, _: msg.answer(
            get_message(ui_lang, "language_cmd"),
            reply_markup=get_ui_language_keyboard(ui_lang)
        ),
        message,
        {"bot": message.bot}
    )

@router.message(Command("translate", "tr"))
async def cmd_translate(message: Message):
    """
    Handle the /translate command to start translation flow.
    
    Args:
        message: Telegram message object
    """
    user_id = message.from_user.id
    
    # Get user preferred language
    user_data = await get_user(user_id)
    ui_lang = user_data["ui_lang"] if user_data and "ui_lang" in user_data else "en"
    
    # Check subscription
    await check_subscription_middleware(
        lambda msg, _: msg.answer(
            get_message(ui_lang, "select_source"),
            reply_markup=get_language_keyboard()
        ),
        message,
        {"bot": message.bot}
    )

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """
    Handle the /stats command (admin only).
    
    Args:
        message: Telegram message object
    """
    user_id = message.from_user.id
    
    # Check if user is admin
    if str(user_id) not in ADMIN_IDS:
        return
    
    # Get user preferred language
    user_data = await get_user(user_id)
    ui_lang = user_data["ui_lang"] if user_data and "ui_lang" in user_data else "en"
    
    # Get statistics
    stats = await get_stats()
    
    # Format stats message
    stats_message = get_message(
        ui_lang, 
        "stats", 
        total_users=stats["total_users"], 
        english_ui=stats["english_ui"], 
        arabic_ui=stats["arabic_ui"],
        subscribed_users=stats["subscribed_users"]
    )
    
    await message.answer(stats_message)
    
@router.callback_query(F.data.startswith("lang_"))
async def process_language_callback(callback: CallbackQuery):
    """
    Handle language selection callback.
    
    Args:
        callback: Callback query object
    """
    user_id = callback.from_user.id
    lang_code = callback.data.split('_')[1]
    
    # Update user's interface language in database
    await update_user_language(user_id, lang_code)
    
    await callback.message.edit_reply_markup(reply_markup=get_ui_language_keyboard(lang_code))
    await callback.message.answer(get_message(lang_code, "language_selected"))
    await callback.answer()

@router.callback_query(F.data.startswith("source_"))
async def process_source_language_callback(callback: CallbackQuery):
    """
    Handle source language selection callback.
    
    Args:
        callback: Callback query object
    """
    user_id = callback.from_user.id
    source_lang_code = callback.data.split('_')[1]
    
    # Get current user
    user_data = await get_user(user_id)
    ui_lang = user_data["ui_lang"] if user_data and "ui_lang" in user_data else "en"
    
    # Check subscription before proceeding
    is_subscribed = await check_user_subscription(callback.bot, user_id)
    if not is_subscribed:
        # Update user's subscription status
        await update_subscription_status(user_id, False)
        
        # Create channel links list
        channel_links = ""
        for channel in config.required_channels:
            # Extract channel username/ID for display
            if channel.startswith('@'):
                channel_name = channel
                channel_link = f"https://t.me/{channel[1:]}"
            else:
                try:
                    chat = await callback.bot.get_chat(channel)
                    channel_name = chat.title or channel
                    if chat.username:
                        channel_link = f"https://t.me/{chat.username}"
                    else:
                        channel_link = f"Channel ID: {channel}"
                except Exception as e:
                    logging.error(f"Error getting channel info: {e}")
                    channel_name = channel
                    channel_link = f"Channel ID: {channel}"
            
            channel_links += f"• <a href='{channel_link}'>{channel_name}</a>\n"
        
        await callback.message.edit_text(
            get_message(ui_lang, "subscription_required", channel_links=channel_links),
            reply_markup=get_subscription_keyboard(ui_lang),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        await callback.answer()
        return
        
    # Show target language selection keyboard
    source_lang_name = LANGUAGES[source_lang_code]
    localized_source_lang = localize_language_names(ui_lang, source_lang_name, "")[0]
    
    await callback.message.edit_text(
        get_message(ui_lang, "selected_source", source_lang=localized_source_lang),
        reply_markup=get_target_language_keyboard(source_lang_code)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("target_"))
async def process_target_language_callback(callback: CallbackQuery):
    """
    Handle target language selection callback.
    
    Args:
        callback: Callback query object
    """
    user_id = callback.from_user.id
    parts = callback.data.split('_')
    source_lang_code = parts[1]
    target_lang_code = parts[2]
    
    # Get current user
    user_data = await get_user(user_id)
    ui_lang = user_data["ui_lang"] if user_data and "ui_lang" in user_data else "en"
    
    # Check subscription before proceeding
    is_subscribed = await check_user_subscription(callback.bot, user_id)
    if not is_subscribed:
        # Update user's subscription status
        await update_subscription_status(user_id, False)
        
        # Create channel links list
        channel_links = ""
        for channel in config.required_channels:
            # Extract channel username/ID for display
            if channel.startswith('@'):
                channel_name = channel
                channel_link = f"https://t.me/{channel[1:]}"
            else:
                try:
                    chat = await callback.bot.get_chat(channel)
                    channel_name = chat.title or channel
                    if chat.username:
                        channel_link = f"https://t.me/{chat.username}"
                    else:
                        channel_link = f"Channel ID: {channel}"
                except Exception as e:
                    logging.error(f"Error getting channel info: {e}")
                    channel_name = channel
                    channel_link = f"Channel ID: {channel}"
            
            channel_links += f"• <a href='{channel_link}'>{channel_name}</a>\n"
        
        await callback.message.edit_text(
            get_message(ui_lang, "subscription_required", channel_links=channel_links),
            reply_markup=get_subscription_keyboard(ui_lang),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        await callback.answer()
        return
    
    # Store user's translation direction
    user_states[user_id] = {
        "source_lang_code": source_lang_code,
        "target_lang_code": target_lang_code
    }
    
    source_lang_name = LANGUAGES[source_lang_code]
    target_lang_name = LANGUAGES[target_lang_code]
    
    # Localize language names
    source_lang_name, target_lang_name = localize_language_names(ui_lang, source_lang_name, target_lang_name)
    
    await callback.message.edit_text(
        get_message(ui_lang, "selected", from_lang=source_lang_name, to_lang=target_lang_name)
    )
    await callback.answer()

@router.callback_query(F.data == "check_subscription")
async def process_check_subscription_callback(callback: CallbackQuery):
    """
    Handle subscription check button callback.
    
    Args:
        callback: Callback query object
    """
    user_id = callback.from_user.id
    
    # Get user from database
    user_data = await get_user(user_id)
    ui_lang = user_data["ui_lang"] if user_data and "ui_lang" in user_data else "en"
    
    # Check subscription status
    is_subscribed = await check_user_subscription(callback.bot, user_id)
    
    if is_subscribed:
        # Update user's subscription status
        await update_subscription_status(user_id, True)
        
        await callback.message.edit_text(
            get_message(ui_lang, "subscription_verified"),
            disable_web_page_preview=True
        )
        
        # Send welcome message with language keyboard
        await callback.message.answer(
            get_message(ui_lang, "welcome"),
            reply_markup=get_language_keyboard()
        )
    else:
        # Update user's subscription status
        await update_subscription_status(user_id, False)
        
        # Create channel links list
        channel_links = ""
        for channel in config.required_channels:
            # Extract channel username/ID for display
            if channel.startswith('@'):
                channel_name = channel
                channel_link = f"https://t.me/{channel[1:]}"
            else:
                try:
                    chat = await callback.bot.get_chat(channel)
                    channel_name = chat.title or channel
                    if chat.username:
                        channel_link = f"https://t.me/{chat.username}"
                    else:
                        channel_link = f"Channel ID: {channel}"
                except Exception as e:
                    logging.error(f"Error getting channel info: {e}")
                    channel_name = channel
                    channel_link = f"Channel ID: {channel}"
            
            channel_links += f"• <a href='{channel_link}'>{channel_name}</a>\n"
        
        await callback.message.edit_text(
            get_message(ui_lang, "subscription_not_verified", channel_links=channel_links),
            reply_markup=get_subscription_keyboard(ui_lang),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    
    await callback.answer()

@router.callback_query(F.data == "ignore")
async def process_ignore_callback(callback: CallbackQuery):
    """
    Handle ignore callback for title buttons.
    
    Args:
        callback: Callback query object
    """
    await callback.answer()

@router.message()
async def translate_message(message: Message):
    """
    Handle text messages and translate them.
    
    Args:
        message: Telegram message object
    """
    user_id = message.from_user.id
    
    # Get user from database
    user_data = await get_user(user_id)
    ui_lang = user_data["ui_lang"] if user_data and "ui_lang" in user_data else "en"
    
    # Check subscription before proceeding
    is_subscribed = await check_user_subscription(message.bot, user_id)
    if not is_subscribed:
        # Update user's subscription status
        await update_subscription_status(user_id, False)
        
        # Create channel links list
        channel_links = ""
        for channel in config.required_channels:
            # Extract channel username/ID for display
            if channel.startswith('@'):
                channel_name = channel
                channel_link = f"https://t.me/{channel[1:]}"
            else:
                try:
                    chat = await message.bot.get_chat(channel)
                    channel_name = chat.title or channel
                    if chat.username:
                        channel_link = f"https://t.me/{chat.username}"
                    else:
                        channel_link = f"Channel ID: {channel}"
                except Exception as e:
                    logging.error(f"Error getting channel info: {e}")
                    channel_name = channel
                    channel_link = f"Channel ID: {channel}"
            
            channel_links += f"• <a href='{channel_link}'>{channel_name}</a>\n"
        
        await message.answer(
            get_message(ui_lang, "subscription_required", channel_links=channel_links),
            reply_markup=get_subscription_keyboard(ui_lang),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        return
    
    # If we got here, the user is subscribed
    await update_subscription_status(user_id, True)
    
    if user_id not in user_states:
        await message.answer(
            get_message(ui_lang, "select_first"),
            reply_markup=get_language_keyboard()
        )
        return
    
    text = message.text
    if len(text) > 2000:
        await message.answer(get_message(ui_lang, "text_too_long"))
        return
    
    source_lang_code = user_states[user_id]["source_lang_code"]
    target_lang_code = user_states[user_id]["target_lang_code"]
    source_lang = LANGUAGES[source_lang_code]
    target_lang = LANGUAGES[target_lang_code]
    
    try:
        translated_text = await translate_text(text, source_lang, target_lang)
        await message.answer(translated_text)
    except Exception as e:
        logging.error(f"Translation error: {e}")
        await message.answer(get_message(ui_lang, "error")) 