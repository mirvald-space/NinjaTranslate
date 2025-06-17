"""
Translation service for the NinjaTranslate bot.
"""
import json
import logging
import aiohttp
from config import config

# List of most common languages with emoji flags
LANGUAGES = {
    "en": "🇬🇧 English",
    "ar": "🇸🇦 Arabic",
    "es": "🇪🇸 Spanish",
    "fr": "🇫🇷 French",
    "de": "🇩🇪 German",
    "zh": "🇨🇳 Chinese",
    "ru": "🇷🇺 Russian",
    "pt": "🇵🇹 Portuguese",
    "ja": "🇯🇵 Japanese",
    "it": "🇮🇹 Italian",
    "ko": "🇰🇷 Korean",
    "tr": "🇹🇷 Turkish",
    "nl": "🇳🇱 Dutch",
    "sv": "🇸🇪 Swedish",
    "pl": "🇵🇱 Polish",
    "vi": "🇻🇳 Vietnamese",
    "hi": "🇮🇳 Hindi",
    "uk": "🇺🇦 Ukrainian"
}

# There are no predefined translation directions anymore
# The user will select source and target languages separately
TRANSLATIONS = {}

# Localized language names for Arabic UI
AR_LANG_NAMES = {
    "🇬🇧 English": "🇬🇧 الإنجليزية",
    "🇸🇦 Arabic": "🇸🇦 العربية",
    "🇪🇸 Spanish": "🇪🇸 الإسبانية",
    "🇫🇷 French": "🇫🇷 الفرنسية",
    "🇩🇪 German": "🇩🇪 الألمانية",
    "🇨🇳 Chinese": "🇨🇳 الصينية",
    "🇷🇺 Russian": "🇷🇺 الروسية",
    "🇵🇹 Portuguese": "🇵🇹 البرتغالية",
    "🇯🇵 Japanese": "🇯🇵 اليابانية",
    "🇮🇹 Italian": "🇮🇹 الإيطالية",
    "🇰🇷 Korean": "🇰🇷 الكورية",
    "🇹🇷 Turkish": "🇹🇷 التركية",
    "🇳🇱 Dutch": "🇳🇱 الهولندية",
    "🇸🇪 Swedish": "🇸🇪 السويدية",
    "🇵🇱 Polish": "🇵🇱 البولندية",
    "🇻🇳 Vietnamese": "🇻🇳 الفيتنامية",
    "🇮🇳 Hindi": "🇮🇳 الهندية",
    "🇺🇦 Ukrainian": "🇺🇦 الأوكرانية"
}

async def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate text using X.AI API.
    
    Args:
        text: Text to translate
        source_lang: Source language
        target_lang: Target language
        
    Returns:
        Translated text
        
    Raises:
        Exception: If translation fails
    """
    # Extract just the language name without the emoji
    source_lang_name = source_lang.split(" ", 1)[1] if " " in source_lang else source_lang
    target_lang_name = target_lang.split(" ", 1)[1] if " " in target_lang else target_lang
    
    headers = {
        "Authorization": f"Bearer {config.xai_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "grok-3-latest",
        "messages": [
            {
                "role": "system",
                "content": f"You are a professional translator. Translate the following text from {source_lang_name} to {target_lang_name}. Return only the translated text without explanations or additional comments. If you can't identify the language, respond with the original text."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "temperature": 0.3,
        "stream": False
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(config.xai_api_url, headers=headers, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API error: {response.status}, {error_text}")
                
                result = await response.json()
                return result["choices"][0]["message"]["content"]
        except aiohttp.ClientError as e:
            logging.error(f"HTTP request error: {e}")
            raise Exception("Network error while connecting to translation service")
        except json.JSONDecodeError:
            logging.error("JSON parsing error")
            raise Exception("Error parsing translation response")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise Exception("Unexpected error during translation") 