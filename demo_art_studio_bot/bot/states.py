from aiogram.fsm.state import State, StatesGroup


class BookingStates(StatesGroup):
    direction = State()
    format = State()
    slot = State()
    name = State()
    contact = State()
    comment = State()
    confirm = State()


class RescheduleStates(StatesGroup):
    action = State()
    contact = State()
    details = State()


class GiftStates(StatesGroup):
    amount = State()
    recipient = State()
    buyer_contact = State()
    wish = State()


class QuizStates(StatesGroup):
    audience = State()
    level = State()
    goal = State()
