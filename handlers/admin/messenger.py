from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from state.sendler import Messenger
from utils.database import Database
import os
import asyncio


async def start_create(message: Message, bot: Bot, state: FSMContext):
    msg = "Веддите текст для рассылки вашим подписчикам"
    await state.set_state(Messenger.messtext)
    await bot.send_message(message.from_user.id, msg)




async def create_mailing(message: Message, bot: Bot, state: FSMContext):
    try:
        await state.update_data(messtext=message.text)
        messanger_data = await state.get_data()
        sms_text = messanger_data.get('messtext')

        db = Database(os.getenv('DATABASE_NAME'))
        sms_id = 1
        sms = db.add_or_update_sms(sms_id, sms_text)
        await bot.send_message(message.from_user.id, f"Текст рассылки успешно добавлен\n"
                                                     f"Новый текст: {sms_text}")
        await state.clear()
    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при попытке обновить рассылку - {error}\n"
            error_file.write(error_message)
            print(f"При попытке обновить рассылку {error}")




async def mailing_list_launch(message: Message, bot: Bot):
    try:
        db = Database(os.getenv('DATABASE_NAME'))
        users = db.get_user()
        sms = db.get_message()
        sms_text = sms[0][1]
        for user in users:
            user_id = user[1]
            sendler_status = await bot.send_message(user_id, sms_text)
            await asyncio.sleep(2)
    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка не удалось получить список пользователей - {error}\n"
            error_file.write(error_message)
            print(f'Не удалось получить список пользователей: {error}')

