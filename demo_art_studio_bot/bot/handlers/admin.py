from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..keyboards import main_menu_keyboard
from ..texts import Texts

router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message, texts: Texts) -> None:
    await message.answer(texts.help, reply_markup=main_menu_keyboard())


@router.message(Command("demo"))
async def cmd_demo(message: Message, texts: Texts) -> None:
    await message.answer(texts.demo, reply_markup=main_menu_keyboard())


@router.message()
async def fallback(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Не совсем понял сообщение. Вот главное меню:",
        reply_markup=main_menu_keyboard(),
    )
