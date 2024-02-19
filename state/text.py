from aiogram.fsm.state import StatesGroup, State

class TextState(StatesGroup):
    text_message = State()