from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🦊"),
        ],
        [
            KeyboardButton(text="🐻")
        ],
        [
            KeyboardButton(text="🦁")
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие из меню",
    selective=True
)
