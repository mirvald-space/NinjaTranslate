"""
Localization module for the NinjaTranslate bot.
"""
from bot.translations import AR_LANG_NAMES

# Messages in both languages
MESSAGES = {
    "en": {
        "welcome": "Welcome to NinjaTranslate! Please select source language:",
        "selected": "Selected {from_lang} → {to_lang} translation.\nSend me text to translate (max 2000 characters).",
        "selected_source": "Source language: {source_lang}\nNow select target language:",
        "select_source": "Please select source language:",
        "select_first": "Please select source language first:",
        "text_too_long": "Text is too long. Maximum is 2000 characters.",
        "error": "Error during translation. Please try again later.",
        "language_cmd": "Select interface language:",
        "language_selected": "Interface language set to English.",
        "stats": "📊 Bot Statistics\n\n👥 Total Users: {total_users}\n🇬🇧 English UI: {english_ui}\n🇸🇦 Arabic UI: {arabic_ui}\n💫 Subscribed Users: {subscribed_users}",
        "subscription_required": "⚠️ Subscription Required ⚠️\n\nTo use NinjaTranslate bot, you need to subscribe to the following channels:\n\n{channel_links}\n\nAfter subscribing, click the \"Check Subscription\" button below.",
        "subscription_check": "Check Subscription",
        "subscription_verified": "✅ Thank you! Your subscription has been verified. You can now use the bot.",
        "subscription_not_verified": "❌ You need to subscribe to all required channels to use the bot.\n\nPlease subscribe to:\n\n{channel_links}\n\nAfter subscribing, click the \"Check Subscription\" button again."
    },
    "ar": {
        "welcome": "مرحبًا بك في NinjaTranslate! يرجى اختيار لغة المصدر:",
        "selected": "تم اختيار الترجمة من {from_lang} إلى {to_lang}.\nأرسل لي النص المراد ترجمته (بحد أقصى 2000 حرف).",
        "selected_source": "لغة المصدر: {source_lang}\nاختر الآن لغة الهدف:",
        "select_source": "يرجى اختيار لغة المصدر:",
        "select_first": "يرجى اختيار لغة المصدر أولاً:",
        "text_too_long": "النص طويل جدًا. الحد الأقصى هو 2000 حرف.",
        "error": "حدث خطأ أثناء الترجمة. يرجى المحاولة مرة أخرى لاحقًا.",
        "language_cmd": "اختر لغة الواجهة:",
        "language_selected": "تم ضبط لغة الواجهة على العربية.",
        "stats": "📊 إحصائيات البوت\n\n👥 إجمالي المستخدمين: {total_users}\n🇬🇧 واجهة إنجليزية: {english_ui}\n🇸🇦 واجهة عربية: {arabic_ui}\n💫 المستخدمون المشتركون: {subscribed_users}",
        "subscription_required": "⚠️ الاشتراك مطلوب ⚠️\n\nلاستخدام بوت NinjaTranslate، يجب عليك الاشتراك في القنوات التالية:\n\n{channel_links}\n\nبعد الاشتراك، انقر على زر \"التحقق من الاشتراك\" أدناه.",
        "subscription_check": "التحقق من الاشتراك",
        "subscription_verified": "✅ شكراً لك! تم التحقق من اشتراكك. يمكنك الآن استخدام البوت.",
        "subscription_not_verified": "❌ يجب عليك الاشتراك في جميع القنوات المطلوبة لاستخدام البوت.\n\nيرجى الاشتراك في:\n\n{channel_links}\n\nبعد الاشتراك، انقر على زر \"التحقق من الاشتراك\" مرة أخرى."
    }
}

# Language names in both languages
LANGUAGE_NAMES = {
    "en": {
        "en": "English",
        "ar": "Arabic"
    },
    "ar": {
        "en": "الإنجليزية",
        "ar": "العربية"
    }
}

def get_message(lang: str, key: str, **kwargs) -> str:
    """
    Get a localized message.
    
    Args:
        lang: Language code (en/ar)
        key: Message key
        **kwargs: Format parameters
        
    Returns:
        Localized message
    """
    message = MESSAGES.get(lang, MESSAGES["en"]).get(key, MESSAGES["en"][key])
    if kwargs:
        return message.format(**kwargs)
    return message
    
def localize_language_names(lang: str, from_lang: str, to_lang: str = None) -> tuple:
    """
    Localize language names for the UI.
    
    Args:
        lang: UI language (en/ar)
        from_lang: Source language name
        to_lang: Target language name
        
    Returns:
        Tuple of localized language names
    """
    if lang == "ar":
        from_lang = AR_LANG_NAMES.get(from_lang, from_lang)
        if to_lang:
            to_lang = AR_LANG_NAMES.get(to_lang, to_lang)
    
    if to_lang is None:
        return (from_lang,)
    return from_lang, to_lang

def get_language_name(ui_lang: str, lang_code: str) -> str:
    """
    Get localized name of a language.
    
    Args:
        ui_lang: UI language (en/ar)
        lang_code: Language code to get name for
        
    Returns:
        Localized language name
    """
    return LANGUAGE_NAMES.get(ui_lang, LANGUAGE_NAMES["en"]).get(lang_code, lang_code) 