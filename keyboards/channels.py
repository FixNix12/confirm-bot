from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

channels_keyboards = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text="Добавить канал")],
        [KeyboardButton(text="Удалить канал")],
        [KeyboardButton(text="Посмотреть список каналов")],
        [KeyboardButton(text="Добавить приветсвие")]
    ],

    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие из меню",
    selective=True
)