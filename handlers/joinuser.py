from aiogram.types import ChatJoinRequest
from aiogram import Bot
import os
from aiogram.types import Message
from keyboards.capcha import main_keyboards
from utils.database import Database
from aiogram.methods.approve_chat_join_request import ApproveChatJoinRequest


pending_users = {}  # Глобальный словарь для хранения chat_id по user_id

async def approve_request(event, bot: Bot):
    user_id = event.from_user.id
    chat_id = event.chat.id
    # Сохраняем chat_id группы для данного user_id
    pending_users[user_id] = chat_id
    msg = "Для того чтобы быть принятым в канал нужно пройти капчу !"
    msg2 = "Нажмите на изображения Льва"
    await bot.send_message(chat_id=user_id, text=f"{msg}\n{msg2}", reply_markup=main_keyboards)




async def approve_user(message: Message, bot: Bot):
    user_id = message.from_user.id
    chat_id = pending_users.get(user_id)

    db = Database(os.getenv('DATABASE_NAME'))
    try:
        if (message.text != "🦁"):
            await bot.send_message(message.from_user.id, f"К сожалению ответ неверный попробуйте еще раз\n"
                                                         f"Найдите льва", reply_markup=main_keyboards)
        else:
            if (message.from_user.username):
                user_name = message.from_user.username
            else:
                user_name = "Not specified"
            user_add = db.add_user(user_id, user_name)
            print(user_add)
            await bot(ApproveChatJoinRequest(chat_id=chat_id, user_id=user_id))
            await bot.send_message(message.from_user.id, f"Поздравляю вы прошли капчу")
    except Exception as error:
            print(f"Ошибка - {error}")


async def object_message(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f' Объект - {message}')
