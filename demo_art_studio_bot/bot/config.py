import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_chat_id: int
    studio_name: str
    studio_address: str
    studio_map_url: str
    studio_phone: str
    studio_hours: str
    studio_instagram: str
    studio_telegram: str


def load_config() -> Config:
    load_dotenv()
    admin_raw = os.environ.get("ADMIN_CHAT_ID", "0")
    try:
        admin_chat_id = int(admin_raw)
    except ValueError:
        logging.warning("Invalid ADMIN_CHAT_ID=%s, fallback to 0", admin_raw)
        admin_chat_id = 0

    return Config(
        bot_token=os.environ.get("BOT_TOKEN", ""),
        admin_chat_id=admin_chat_id,
        studio_name=os.environ.get("STUDIO_NAME", "Art Studio"),
        studio_address=os.environ.get("STUDIO_ADDRESS", ""),
        studio_map_url=os.environ.get("STUDIO_MAP_URL", ""),
        studio_phone=os.environ.get("STUDIO_PHONE", ""),
        studio_hours=os.environ.get("STUDIO_HOURS", ""),
        studio_instagram=os.environ.get("STUDIO_INSTAGRAM", ""),
        studio_telegram=os.environ.get("STUDIO_TELEGRAM", ""),
    )
