import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

class Config(BaseModel):
    bot_token: str = Field(default=os.getenv("BOT_TOKEN"))
    xai_api_key: str = Field(default=os.getenv("XAI_API_KEY"))
    xai_api_url: str = Field(default="https://api.x.ai/v1/chat/completions")
    
    # MongoDB settings
    mongo_uri: str = Field(default=os.getenv("MONGO_URI", "mongodb://localhost:27017"))
    mongo_db: str = Field(default=os.getenv("MONGO_DB", "ninja_translate_bot"))
    
    # Subscription settings
    required_channels: List[str] = Field(
        default=[
            os.getenv("CHANNEL_ID_1", ""),
            os.getenv("CHANNEL_ID_2", "")
        ]
    )
    
    # Time in minutes to recheck subscription status
    subscription_check_interval: int = Field(default=60)
    
    def validate_tokens(self) -> bool:
        return bool(self.bot_token) and bool(self.xai_api_key)
    
    def validate_channels(self) -> bool:
        return all(self.required_channels)

config = Config() 