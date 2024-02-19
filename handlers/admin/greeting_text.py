from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from state.text import TextState
from utils.database import Database
import os


# создание кнопок с выбором канала
async def get_channels_key():
    db = Database(os.getenv('DATABASE_NAME'))
    channels = db.get_channels()

    inline_keyboard = []
    #
    for channel in channels:
        id_channel = channel[0]
        name_channel = channel[2]
        button = InlineKeyboardButton(text=name_channel, callback_data=f"text_channel_id:{id_channel}")  # Передает в параметры кнопки user_name в качестве информации вывода и user_id в качестве callback
        row = [button]
        inline_keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)




async def add_text(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, f'Введите текст для приветствия')
    await state.set_state(TextState.text_message)


async def handler_text(message: Message, bot: Bot, state: FSMContext):
    try:
        message_text = message.text

        await state.update_data(text_message=message_text)

        keyboard = await get_channels_key()
        await bot.send_message(message.from_user.id, "Выберите канал за кем закрепить данный текст:", reply_markup=keyboard)


    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при записи текста - {error}\n"
            error_file.write(error_message)
            print(error_message)


async def choice_channel_text(call: CallbackQuery, state: FSMContext):
    try:
        channel_id = int(call.data.split(":")[1])

        data_state = await state.get_data()
        greeting_text = data_state.get('text_message')


        db = Database(os.getenv('DATABASE_NAME'))
        text_status = db.add_or_update_greeting_text(channel_id, greeting_text)

        await call.message.answer(f'Текст успешно добавлено и закрепленно за каналом')
        await state.clear()

    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при попытке добавить запись текста в базу данных - {error}\n"
            error_file.write(error_message)
            print(error_message)