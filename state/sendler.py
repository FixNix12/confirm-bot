from aiogram.fsm.state import StatesGroup, State

class Messenger(StatesGroup):
    messtext = State()