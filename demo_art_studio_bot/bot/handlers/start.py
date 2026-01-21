from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..keyboards import main_menu_keyboard
from ..texts import Texts

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, texts: Texts) -> None:
    await message.answer(texts.welcome, reply_markup=main_menu_keyboard())
