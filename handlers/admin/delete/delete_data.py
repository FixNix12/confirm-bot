from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from utils.database import Database
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_channels_id(call_value):
    db = Database(os.getenv('DATABASE_NAME'))
    channels = db.get_channels()

    inline_keyboard = []
    #
    for channel in channels:
        id_channel = channel[0]
        name_channel = channel[2]
        button = InlineKeyboardButton(text=name_channel, callback_data=f"{call_value}:{id_channel}")  # Передает в параметры кнопки user_name в качестве информации вывода и user_id в качестве callback
        row = [button]
        inline_keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

async def delete_channel(message: Message, bot: Bot):
    try:
        call_value = "delete_channel"
        keyboards = await get_channels_id(call_value)
        await bot.send_message(message.from_user.id, f"Выберите канал для удаления", reply_markup=keyboards)
    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при функции старта команды удаления delete_channel - {error}\n"
            error_file.write(error_message)
            print(error_message)


async def try_delete_channel(call: CallbackQuery):
    try:
        channel_id = int(call.data.split(":")[1])
        db = Database(os.getenv('DATABASE_NAME'))
        delete_chanel = db.delete_channel_data(channel_id)
        await call.message.answer(f'Канал успешно удален')

    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при удалении канала - {error}\n"
            error_file.write(error_message)
            print(error_message)

async def delete_greeting(message: Message, bot: Bot):
    try:
        call_value = "delete_greeting"
        keyboards = await get_channels_id(call_value)
        await bot.send_message(message.from_user.id, f"Выберите приветствие для удаления", reply_markup=keyboards)
    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при функции старта команды удаления delete_greeting - {error}\n"
            error_file.write(error_message)
            print(error_message)


async def try_delete_greeting(call: CallbackQuery):
    try:
        channel_id = int(call.data.split(":")[1])
        db = Database(os.getenv('DATABASE_NAME'))
        delete_greeting = db.delete_bot_greeting(channel_id)
        await call.message.answer(f'Приветствие успешно удалено')
    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при удалении приветствия - {error}\n"
            error_file.write(error_message)
            print(error_message)

async def delete_messanger(message: Message, bot: Bot):
    try:
        channel_id = 1
        db = Database(os.getenv('DATABASE_NAME'))
        delete_messanger = db.delete_messanger_data(channel_id)
        await bot.send_message(message.from_user.id, f'Рассылка успешно удален')
    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при удалении рассылки - {error}\n"
            error_file.write(error_message)
            print(error_message)

