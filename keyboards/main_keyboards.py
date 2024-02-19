from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="/start",
                placeholder="Нажмите на кнопку start"
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие из меню",
    selective=True
)

main_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Управление приветствием")
        ],
        [
            KeyboardButton(text="Управление рассылкой")
        ],
        [
            KeyboardButton(text="Управление каналами")
        ],
        [
            KeyboardButton(text="Удаление метериала")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие из меню",
    selective=True
)

greeting_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Добавить тект приветствия'
            )
        ],
        [
            KeyboardButton(
                text='Добавить видео приветствия'
            )
        ],
        [
            KeyboardButton(
                text='Добавить кнопку приветствия'
            )
        ],
        [
            KeyboardButton(
                text='Основное меню'
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие с аккаунтом"
)

channels_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Добавить канал'
            )
        ],
        [
            KeyboardButton(
                text='Основное меню'
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

messager_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Добавить тект рассылки'
            )
        ],
        [
            KeyboardButton(
                text='Добавить видео рассылки'
            )
        ],
        [
            KeyboardButton(
                text='Добавить кнопку рассылки'
            )
        ],
        [
            KeyboardButton(
                text="Запустить рассылку"
            )
        ],
        [
            KeyboardButton(
                text='Основное меню'
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие с рассылкой"
)


delete_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Удалить канал")
        ],
        [
            KeyboardButton(text="Удалить приветствие")
        ],
        [
            KeyboardButton(text="Удалить рассылку")
        ],
        [
            KeyboardButton(
                text='Основное меню'
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
