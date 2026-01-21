from aiogram import Router
from aiogram.types import Message

from ..keyboards import MENU_FAQ, MENU_BUTTON, main_menu_keyboard
from ..texts import Texts

router = Router()


@router.message(lambda message: message.text == MENU_FAQ)
async def show_faq(message: Message, texts: Texts) -> None:
    await message.answer(texts.faq, reply_markup=main_menu_keyboard())


@router.message(lambda message: message.text == MENU_BUTTON)
async def back_to_menu(message: Message, texts: Texts) -> None:
    await message.answer("Возвращаю в меню.", reply_markup=main_menu_keyboard())
