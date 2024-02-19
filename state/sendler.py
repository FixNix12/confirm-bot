from aiogram.fsm.state import StatesGroup, State

class MessengerState(StatesGroup):
    mes_text = State()


class MessengerVideoState(StatesGroup):
    mes_video_text = State()