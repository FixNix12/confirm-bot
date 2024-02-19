from aiogram.fsm.state import StatesGroup, State

class ChannelsState(StatesGroup):
    channel_id = State()
    channel_name = State()
    channel_link = State()