"""
Keyboard module for the NinjaTranslate bot.
"""
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.translations import TRANSLATIONS
from bot.localization import get_language_name

def get_language_keyboard():
    """
    Create an inline keyboard with language selection buttons.
    
    Returns:
        Inline keyboard markup with translation direction buttons
    """
    builder = InlineKeyboardBuilder()
    for key, value in TRANSLATIONS.items():
        builder.button(
            text=f"{value['from']}→{value['to']}", 
            callback_data=key
        )
    builder.adjust(2)
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
            lang_name = f"✓ {lang_name}"
            
        builder.button(
            text=lang_name,
            callback_data=f"lang_{lang_code}"
        )
            
    builder.adjust(2)
    return builder.as_markup() 