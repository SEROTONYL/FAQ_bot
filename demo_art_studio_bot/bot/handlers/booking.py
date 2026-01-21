import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..config import Config
from ..keyboards import (
    BACK_BUTTON,
    CANCEL_BUTTON,
    CONFIRM_BUTTON,
    EDIT_BUTTON,
    MENU_BOOKING,
    MENU_GIFT,
    MENU_QUIZ,
    MENU_RESCHEDULE,
    MENU_BUTTON,
    booking_direction_keyboard,
    booking_format_keyboard,
    booking_slot_keyboard,
    confirm_keyboard,
    gift_amount_keyboard,
    main_menu_keyboard,
    navigation_keyboard,
    quiz_audience_keyboard,
    quiz_goal_keyboard,
    quiz_level_keyboard,
    reschedule_action_keyboard,
)
from ..states import BookingStates, GiftStates, QuizStates, RescheduleStates
from ..texts import (
    booking_summary,
    gift_summary,
    quiz_recommendation,
    reschedule_summary,
)
from ..utils.validators import is_valid_contact

router = Router()


async def notify_admin(message: Message, config: Config, text: str) -> None:
    if config.admin_chat_id == 0:
        logging.warning("ADMIN_CHAT_ID is not set; admin notification: %s", text)
        return
    await message.bot.send_message(config.admin_chat_id, text)


def user_info(message: Message) -> str:
    username = message.from_user.username or "без username"
    return f"tg_id: {message.from_user.id}, username: @{username}"


@router.message(Command("cancel"))
async def cancel_any(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Действие отменено. Возвращаю в меню.", reply_markup=main_menu_keyboard())


@router.message(lambda message: message.text == CANCEL_BUTTON)
async def cancel_button(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Действие отменено. Возвращаю в меню.", reply_markup=main_menu_keyboard())


@router.message(lambda message: message.text == MENU_BOOKING)
async def start_booking(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(BookingStates.direction)
    await message.answer("Выберите направление:", reply_markup=booking_direction_keyboard())


@router.message(BookingStates.direction)
async def booking_direction(message: Message, state: FSMContext) -> None:
    if message.text == BACK_BUTTON:
        await state.clear()
        await message.answer("Главное меню.", reply_markup=main_menu_keyboard())
        return
    await state.update_data(direction=message.text)
    await state.set_state(BookingStates.format)
    await message.answer("Выберите формат:", reply_markup=booking_format_keyboard())


@router.message(BookingStates.format)
async def booking_format(message: Message, state: FSMContext) -> None:
    if message.text == BACK_BUTTON:
        await state.set_state(BookingStates.direction)
        await message.answer("Выберите направление:", reply_markup=booking_direction_keyboard())
        return
    await state.update_data(format=message.text)
    await state.set_state(BookingStates.slot)
    await message.answer("Выберите удобное время:", reply_markup=booking_slot_keyboard())


@router.message(BookingStates.slot)
async def booking_slot(message: Message, state: FSMContext) -> None:
    if message.text == BACK_BUTTON:
        await state.set_state(BookingStates.format)
        await message.answer("Выберите формат:", reply_markup=booking_format_keyboard())
        return
    await state.update_data(slot=message.text)
    await state.set_state(BookingStates.name)
    await message.answer("Как вас зовут?", reply_markup=navigation_keyboard())


@router.message(BookingStates.name)
async def booking_name(message: Message, state: FSMContext) -> None:
    if message.text == BACK_BUTTON:
        await state.set_state(BookingStates.slot)
        await message.answer("Выберите удобное время:", reply_markup=booking_slot_keyboard())
        return
    await state.update_data(name=message.text)
    await state.set_state(BookingStates.contact)
    await message.answer("Оставьте контакт (телефон или @username):", reply_markup=navigation_keyboard())


@router.message(BookingStates.contact)
async def booking_contact(message: Message, state: FSMContext) -> None:
    if message.text == BACK_BUTTON:
        await state.set_state(BookingStates.name)
        await message.answer("Как вас зовут?", reply_markup=navigation_keyboard())
        return
    if not is_valid_contact(message.text):
        await message.answer("Пожалуйста, укажите телефон или @username.")
        return
    await state.update_data(contact=message.text)
    await state.set_state(BookingStates.comment)
    await message.answer("Комментарий или пожелания? (можно пропустить)", reply_markup=navigation_keyboard())


@router.message(BookingStates.comment)
async def booking_comment(message: Message, state: FSMContext) -> None:
    if message.text == BACK_BUTTON:
        await state.set_state(BookingStates.contact)
        await message.answer("Оставьте контакт (телефон или @username):", reply_markup=navigation_keyboard())
        return
    await state.update_data(comment=message.text)
    data = await state.get_data()
    await state.set_state(BookingStates.confirm)
    await message.answer(booking_summary(data), reply_markup=confirm_keyboard())


@router.message(BookingStates.confirm)
async def booking_confirm(message: Message, state: FSMContext, config: Config) -> None:
    if message.text == EDIT_BUTTON:
        await state.set_state(BookingStates.direction)
        await message.answer("Давайте начнём сначала. Выберите направление:", reply_markup=booking_direction_keyboard())
        return
    if message.text == CONFIRM_BUTTON:
        data = await state.get_data()
        text = (
            "Новая заявка на запись:\n"
            f"Направление: {data.get('direction')}\n"
            f"Формат: {data.get('format')}\n"
            f"Слот: {data.get('slot')}\n"
            f"Имя: {data.get('name')}\n"
            f"Контакт: {data.get('contact')}\n"
            f"Комментарий: {data.get('comment') or '—'}\n"
            f"{user_info(message)}"
        )
        await notify_admin(message, config, text)
        await state.clear()
        await message.answer("Спасибо! Мы свяжемся с вами для подтверждения.", reply_markup=main_menu_keyboard())
        return
    if message.text == BACK_BUTTON:
        await state.set_state(BookingStates.comment)
        await message.answer("Комментарий или пожелания? (можно пропустить)", reply_markup=navigation_keyboard())
        return
    await message.answer("Выберите один из вариантов ниже.", reply_markup=confirm_keyboard())


@router.message(lambda message: message.text == MENU_RESCHEDULE)
async def start_reschedule(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(RescheduleStates.action)
    await message.answer("Что нужно сделать?", reply_markup=reschedule_action_keyboard())


@router.message(RescheduleStates.action)
async def reschedule_action(message: Message, state: FSMContext) -> None:
    if message.text == BACK_BUTTON:
        await state.clear()
        await message.answer("Главное меню.", reply_markup=main_menu_keyboard())
        return
    await state.update_data(action=message.text)
    await state.set_state(RescheduleStates.contact)
    await message.answer("Оставьте контакт для связи:", reply_markup=navigation_keyboard())


@router.message(RescheduleStates.contact)
async def reschedule_contact(message: Message, state: FSMContext) -> None:
    if message.text == BACK_BUTTON:
        await state.set_state(RescheduleStates.action)
        await message.answer("Что нужно сделать?", reply_markup=reschedule_action_keyboard())
        return
    if not is_valid_contact(message.text):
        await message.answer("Пожалуйста, укажите телефон или @username.")
        return
    await state.update_data(contact=message.text)
    await state.set_state(RescheduleStates.details)
    await message.answer("Опишите причину или желаемое время.", reply_markup=navigation_keyboard())


@router.message(RescheduleStates.details)
async def reschedule_details(message: Message, state: FSMContext, config: Config) -> None:
    if message.text == BACK_BUTTON:
        await state.set_state(RescheduleStates.contact)
        await message.answer("Оставьте контакт для связи:", reply_markup=navigation_keyboard())
        return
    await state.update_data(details=message.text)
    data = await state.get_data()
    text = reschedule_summary(data) + f"\n{user_info(message)}"
    await notify_admin(message, config, text)
    await state.clear()
    await message.answer("Заявка отправлена. Мы напишем вам в ближайшее время.", reply_markup=main_menu_keyboard())


@router.message(lambda message: message.text == MENU_GIFT)
async def start_gift(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(GiftStates.amount)
    await state.update_data(awaiting_custom_amount=False)
    await message.answer("Выберите номинал сертификата:", reply_markup=gift_amount_keyboard())


@router.message(GiftStates.amount)
async def gift_amount(message: Message, state: FSMContext) -> None:
    if message.text == BACK_BUTTON:
        await state.clear()
        await message.answer("Главное меню.", reply_markup=main_menu_keyboard())
        return
    data = await state.get_data()
    if data.get("awaiting_custom_amount"):
        await state.update_data(amount=message.text, awaiting_custom_amount=False)
        await state.set_state(GiftStates.recipient)
        await message.answer("Кому сертификат?", reply_markup=navigation_keyboard())
        return
    if message.text == "Другой":
        await state.update_data(awaiting_custom_amount=True)
        await message.answer("Введите желаемую сумму:")
        return
    await state.update_data(amount=message.text)
    await state.set_state(GiftStates.recipient)
    await message.answer("Кому сертификат?", reply_markup=navigation_keyboard())


@router.message(GiftStates.recipient)
async def gift_recipient(message: Message, state: FSMContext) -> None:
    if message.text == BACK_BUTTON:
        await state.set_state(GiftStates.amount)
        await message.answer("Выберите номинал сертификата:", reply_markup=gift_amount_keyboard())
        return
    await state.update_data(recipient=message.text)
    await state.set_state(GiftStates.buyer_contact)
    await message.answer("Контакт покупателя:", reply_markup=navigation_keyboard())


@router.message(GiftStates.buyer_contact)
async def gift_contact(message: Message, state: FSMContext) -> None:
    if message.text == BACK_BUTTON:
        await state.set_state(GiftStates.recipient)
        await message.answer("Кому сертификат?", reply_markup=navigation_keyboard())
        return
    if not is_valid_contact(message.text):
        await message.answer("Пожалуйста, укажите телефон или @username.")
        return
    await state.update_data(buyer_contact=message.text)
    await state.set_state(GiftStates.wish)
    await message.answer("Пожелание к сертификату? (можно пропустить)", reply_markup=navigation_keyboard())


@router.message(GiftStates.wish)
async def gift_wish(message: Message, state: FSMContext, config: Config) -> None:
    if message.text == BACK_BUTTON:
        await state.set_state(GiftStates.buyer_contact)
        await message.answer("Контакт покупателя:", reply_markup=navigation_keyboard())
        return
    await state.update_data(wish=message.text)
    data = await state.get_data()
    text = gift_summary(data) + f"\n{user_info(message)}"
    await notify_admin(message, config, text)
    await state.clear()
    await message.answer("Спасибо! Мы свяжемся с вами по сертификату.", reply_markup=main_menu_keyboard())


@router.message(lambda message: message.text == MENU_QUIZ)
async def start_quiz(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(QuizStates.audience)
    await message.answer("Кто будет заниматься?", reply_markup=quiz_audience_keyboard())


@router.message(QuizStates.audience)
async def quiz_audience(message: Message, state: FSMContext) -> None:
    if message.text == BACK_BUTTON:
        await state.clear()
        await message.answer("Главное меню.", reply_markup=main_menu_keyboard())
        return
    await state.update_data(audience=message.text)
    await state.set_state(QuizStates.level)
    await message.answer("Уровень подготовки?", reply_markup=quiz_level_keyboard())


@router.message(QuizStates.level)
async def quiz_level(message: Message, state: FSMContext) -> None:
    if message.text == BACK_BUTTON:
        await state.set_state(QuizStates.audience)
        await message.answer("Кто будет заниматься?", reply_markup=quiz_audience_keyboard())
        return
    await state.update_data(level=message.text)
    await state.set_state(QuizStates.goal)
    await message.answer("Цель занятий?", reply_markup=quiz_goal_keyboard())


@router.message(QuizStates.goal)
async def quiz_goal(message: Message, state: FSMContext) -> None:
    if message.text == BACK_BUTTON:
        await state.set_state(QuizStates.level)
        await message.answer("Уровень подготовки?", reply_markup=quiz_level_keyboard())
        return
    await state.update_data(goal=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer(
        f"{quiz_recommendation(data)}\n\nГотовы записаться? Нажмите “{MENU_BOOKING}”.",
        reply_markup=main_menu_keyboard(),
    )
