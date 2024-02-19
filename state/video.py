from aiogram.fsm.state import StatesGroup, State

class VideoState(StatesGroup):
    video_file = State()