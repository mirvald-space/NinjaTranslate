"""
Translation service for the NinjaTranslate bot.
"""
import json
import logging
import aiohttp
from config import config

# Translation directions
TRANSLATIONS = {
    "ar_en": {"from": "Arabic", "to": "English"},
    "en_ar": {"from": "English", "to": "Arabic"}
}

# Arabic language names
AR_LANG_NAMES = {
    "Arabic": "العربية",
    "English": "الإنجليزية"
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
    headers = {
        "Authorization": f"Bearer {config.xai_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "grok-3-latest",
        "messages": [
            {
                "role": "system",
                "content": f"You are a professional translator. Translate the following text from {source_lang} to {target_lang}. Return only the translated text without explanations or additional comments."
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