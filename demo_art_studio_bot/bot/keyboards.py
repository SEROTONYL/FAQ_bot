from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

MENU_BOOKING = "🎨 Записаться"
MENU_SCHEDULE = "📅 Расписание"
MENU_PRICES = "💳 Цены / Абонементы"
MENU_ADDRESS = "📍 Адрес / Как пройти"
MENU_GIFT = "🎁 Подарочный сертификат"
MENU_QUIZ = "🧠 Подобрать занятие"
MENU_FAQ = "❓ Вопросы (FAQ)"
MENU_RESCHEDULE = "🔄 Перенести / отменить запись"
MENU_CONTACTS = "📞 Контакты"

BACK_BUTTON = "⬅️ Назад"
MENU_BUTTON = "🏠 В меню"

CONFIRM_BUTTON = "✅ Подтвердить"
EDIT_BUTTON = "✏️ Исправить"
CANCEL_BUTTON = "❌ Отмена"


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MENU_BOOKING), KeyboardButton(text=MENU_SCHEDULE)],
            [KeyboardButton(text=MENU_PRICES), KeyboardButton(text=MENU_ADDRESS)],
            [KeyboardButton(text=MENU_GIFT), KeyboardButton(text=MENU_QUIZ)],
            [KeyboardButton(text=MENU_FAQ), KeyboardButton(text=MENU_RESCHEDULE)],
            [KeyboardButton(text=MENU_CONTACTS)],
        ],
        resize_keyboard=True,
    )


def navigation_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BACK_BUTTON), KeyboardButton(text=MENU_BUTTON)]],
        resize_keyboard=True,
    )


def booking_direction_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Скетчинг"), KeyboardButton(text="Акварель")],
            [KeyboardButton(text="Комиксы"), KeyboardButton(text="Детская группа")],
            [KeyboardButton(text="Другое")],
            [KeyboardButton(text=BACK_BUTTON), KeyboardButton(text=MENU_BUTTON)],
        ],
        resize_keyboard=True,
    )


def booking_format_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Пробное"), KeyboardButton(text="Разовое")],
            [KeyboardButton(text="Абонемент")],
            [KeyboardButton(text=BACK_BUTTON), KeyboardButton(text=MENU_BUTTON)],
        ],
        resize_keyboard=True,
    )


def booking_slot_keyboard() -> ReplyKeyboardMarkup:
    slots = [
        "Сегодня 19:00",
        "Сегодня 20:00",
        "Завтра 18:30",
        "Завтра 19:00",
        "Сб 12:00",
        "Сб 14:00",
        "Вс 11:00",
        "Вс 16:00",
    ]
    rows = [[KeyboardButton(text=slot)] for slot in slots]
    rows.append([KeyboardButton(text=BACK_BUTTON), KeyboardButton(text=MENU_BUTTON)])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def confirm_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=CONFIRM_BUTTON), KeyboardButton(text=EDIT_BUTTON)],
                  [KeyboardButton(text=CANCEL_BUTTON), KeyboardButton(text=MENU_BUTTON)]],
        resize_keyboard=True,
    )


def reschedule_action_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отмена"), KeyboardButton(text="Перенос")],
            [KeyboardButton(text=BACK_BUTTON), KeyboardButton(text=MENU_BUTTON)],
        ],
        resize_keyboard=True,
    )


def gift_amount_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1500"), KeyboardButton(text="3000")],
            [KeyboardButton(text="5000"), KeyboardButton(text="Другой")],
            [KeyboardButton(text=BACK_BUTTON), KeyboardButton(text=MENU_BUTTON)],
        ],
        resize_keyboard=True,
    )


def quiz_audience_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Взрослый"), KeyboardButton(text="Ребёнок")],
            [KeyboardButton(text=BACK_BUTTON), KeyboardButton(text=MENU_BUTTON)],
        ],
        resize_keyboard=True,
    )


def quiz_level_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Новичок"), KeyboardButton(text="Есть опыт")],
            [KeyboardButton(text=BACK_BUTTON), KeyboardButton(text=MENU_BUTTON)],
        ],
        resize_keyboard=True,
    )


def quiz_goal_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Для удовольствия")],
            [KeyboardButton(text="Прокачать навык")],
            [KeyboardButton(text="Подарок")],
            [KeyboardButton(text=BACK_BUTTON), KeyboardButton(text=MENU_BUTTON)],
        ],
        resize_keyboard=True,
    )
