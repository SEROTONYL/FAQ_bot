from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..config import Config
from ..keyboards import (
    MENU_ADDRESS,
    MENU_CONTACTS,
    MENU_PRICES,
    MENU_SCHEDULE,
    MENU_BUTTON,
    main_menu_keyboard,
)
from ..texts import Texts, address_text, contacts_text

router = Router()


@router.message(lambda message: message.text == MENU_SCHEDULE)
async def show_schedule(message: Message, texts: Texts) -> None:
    await message.answer(texts.schedule, reply_markup=main_menu_keyboard())


@router.message(lambda message: message.text == MENU_PRICES)
async def show_prices(message: Message, texts: Texts) -> None:
    await message.answer(texts.prices, reply_markup=main_menu_keyboard())


@router.message(lambda message: message.text == MENU_ADDRESS)
async def show_address(message: Message, config: Config) -> None:
    await message.answer(address_text(config), reply_markup=main_menu_keyboard())


@router.message(lambda message: message.text == MENU_CONTACTS)
async def show_contacts(message: Message, config: Config) -> None:
    await message.answer(contacts_text(config), reply_markup=main_menu_keyboard())


@router.message(lambda message: message.text == MENU_BUTTON)
async def go_menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Главное меню.", reply_markup=main_menu_keyboard())
