import asyncio

from aiogram.types import ChatJoinRequest, FSInputFile
from aiogram import Bot
import os
from aiogram.types import Message
from keyboards.capcha import main_keyboards
from utils.database import Database
from aiogram.methods.approve_chat_join_request import ApproveChatJoinRequest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_channels_key(btn_text, btn_link):

    inline_keyboard = []
    btn_text = btn_text
    btn_link = btn_link
    button = InlineKeyboardButton(text=btn_text, url=btn_link)
    row = [button]
    inline_keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

pending_users = {}  # Глобальный словарь для хранения chat_id по user_id

async def approve_request(event, bot: Bot):
    try:

        user_id = event.from_user.id
        chat_id = event.chat.id

        db = Database(os.getenv('DATABASE_NAME'))
        request_id = db.select_channel_id(chat_id)

        greeting_info = [db.select_channel_info(request_id)]
        greeting_btns = [db.select_channel_btns(request_id)]

        global text_marker
        global video_marker
        global btns_marker


        for greeting_item in greeting_info:
            if greeting_item[0]:
                greeting_text = greeting_item[0]
                text_marker = True
            else:
                greeting_text = ""
                text_marker = False

            if greeting_item[1]:
                greeting_video = greeting_item[1]
                video_marker = True
            else:
                greeting_video = ""
                video_marker = False

        for btn_item in greeting_btns:
            if btn_item[0] and btn_item[1]:
                btn_text = btn_item[0]
                btn_link = btn_item[1]

                channel_invite = await get_channels_key(btn_text, btn_link)

                btns_marker = True
            else:
                btns_marker = False


        if video_marker and text_marker:
            my_video = FSInputFile(greeting_video)
            await bot.send_video(chat_id=user_id, video=my_video, caption=greeting_text)
            await asyncio.sleep(1)
            text_marker = False
            video_marker = False

        if video_marker:
            my_video = FSInputFile(greeting_video) 
            await bot.send_video(chat_id=user_id, video=my_video)
            await asyncio.sleep(1)

        if text_marker:
            await bot.send_message(chat_id=user_id, text=f"{greeting_text}")
            await asyncio.sleep(1)


        if btns_marker:
            await bot.send_message(chat_id=user_id, text=f"Подпишитесь на наши другие проекты", reply_markup=channel_invite)
            await asyncio.sleep(1)



        # Сохраняем chat_id группы для данного user_id
        pending_users[user_id] = chat_id
        msg = "Для того чтобы быть принятым в канал нужно пройти капчу !"
        msg2 = "Нажмите на изображения Льва"
        await bot.send_message(chat_id=user_id, text=f"{msg}\n{msg2}", reply_markup=main_keyboards)

    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при событии вступлении события в канал - {error}\n"
            error_file.write(error_message)
            print(error_message)




async def approve_user(message: Message, bot: Bot):
    user_id = message.from_user.id
    chat_id = pending_users.get(user_id)

    print(f"{user_id}"  
          f"{chat_id}")

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
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при подтверждении пользователя в канал - {error}\n"
            error_file.write(error_message)
            print(error_message)

async def object_message(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f' Объект - {message}')
