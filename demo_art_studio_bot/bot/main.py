import asyncio
import logging

from aiogram import Bot, Dispatcher

from .config import load_config
from .handlers import admin_router, booking_router, faq_router, menu_router, start_router
from .texts import build_texts


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s",
    )
    config = load_config()
    if not config.bot_token:
        raise RuntimeError("BOT_TOKEN is required to запускать бота")

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(booking_router)
    dp.include_router(faq_router)
    dp.include_router(admin_router)

    texts = build_texts(config)

    await dp.start_polling(bot, config=config, texts=texts)


if __name__ == "__main__":
    asyncio.run(main())
