"""
Keyboard module for the NinjaTranslate bot.
"""
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.translations import LANGUAGES
from bot.localization import get_message, get_language_name

def get_language_keyboard():
    """
    Create an inline keyboard to select source language.
    
    Returns:
        Inline keyboard markup with source language buttons
    """
    builder = InlineKeyboardBuilder()
    
    # Title button (not clickable)
    builder.button(
        text="🌍 SELECT SOURCE LANGUAGE 🌍",
        callback_data="ignore"
    )
    
    # Add language buttons, 3 in a row
    for lang_code, lang_name in LANGUAGES.items():
        builder.button(
            text=f"{lang_name}",
            callback_data=f"source_{lang_code}"
        )
    
    builder.adjust(1, 2, 2, 2)  # First row for title, then 2 buttons per row
    return builder.as_markup()

def get_target_language_keyboard(source_lang_code):
    """
    Create an inline keyboard to select target language.
    
    Args:
        source_lang_code: Source language code selected by user
    
    Returns:
        Inline keyboard markup with target language buttons
    """
    builder = InlineKeyboardBuilder()
    
    # Title button (not clickable)
    builder.button(
        text="🎯 SELECT TARGET LANGUAGE 🎯",
        callback_data="ignore"
    )
    
    # Add language buttons, excluding source language
    for lang_code, lang_name in LANGUAGES.items():
        if lang_code != source_lang_code:
            builder.button(
                text=f"{lang_name}",
                callback_data=f"target_{source_lang_code}_{lang_code}"
            )
    
    builder.adjust(1, 2, 2, 2)  # First row for title, then 2 buttons per row
    return builder.as_markup()

def get_ui_language_keyboard(ui_lang: str):
    """
    Create an inline keyboard for UI language selection.
    
    Args:
        ui_lang: Current UI language code
        
    Returns:
        Inline keyboard markup with language options
    """
    builder = InlineKeyboardBuilder()
    
    # Add language buttons
    for lang_code in ["en", "ar"]:
        lang_name = get_language_name(ui_lang, lang_code)
        # Add a ✓ mark to the current language
        if lang_code == ui_lang:
            lang_name = f"✅ {lang_name}"
        
        # Add emoji flags
        flag = "🇬🇧" if lang_code == "en" else "🇸🇦" if lang_code == "ar" else ""
        
        builder.button(
            text=f"{flag} {lang_name}",
            callback_data=f"lang_{lang_code}"
        )
            
    builder.adjust(2)
    return builder.as_markup()

def get_subscription_keyboard(ui_lang: str):
    """
    Create a keyboard with subscription check button.
    
    Args:
        ui_lang: UI language code
        
    Returns:
        Inline keyboard with subscription check button
    """
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text=get_message(ui_lang, "subscription_check"),
        callback_data="check_subscription"
    )
    
    return builder.as_markup() 