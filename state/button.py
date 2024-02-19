from aiogram.fsm.state import StatesGroup, State

class BtnState(StatesGroup):
    btn_text = State()
    btn_link = State()