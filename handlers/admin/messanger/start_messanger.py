from aiogram.types import Message, FSInputFile
from aiogram import Bot
from utils.database import Database
import os
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_channels_key(btn_text, btn_link):

    inline_keyboard = []
    btn_text = btn_text
    btn_link = btn_link
    button = InlineKeyboardButton(text=btn_text, url=btn_link)
    row = [button]
    inline_keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)




async def mailing_list_launch(message: Message, bot: Bot):
    try:
        db = Database(os.getenv('DATABASE_NAME'))
        data_id = 1

        users = db.get_user()

        messanger_info = [db.select_messanger_info(data_id)]
        messanger_btns = [db.select_messanger_btns(data_id)]

        global text_marker
        global video_marker
        global btns_marker


        for messanger_item in messanger_info:
            if messanger_item[0]:
                messanger_text = messanger_item[0]
                text_marker = True
            else:
                messanger_text = ""
                text_marker = False

            if messanger_item[1]:
                messanger_video = messanger_item[1]
                video_marker = True
            else:
                messanger_video = ""
                video_marker = False

        for btn_item in messanger_btns:
            if btn_item[0] and btn_item[1]:
                btn_text = btn_item[0]
                btn_link = btn_item[1]

                channel_invite = await get_channels_key(btn_text, btn_link)

                btns_marker = True
            else:
                btns_marker = False


        if video_marker and text_marker:
            my_video = FSInputFile(messanger_video)
            for user in users:
                user_id = user[1]
                sendler_status = await bot.send_video(chat_id=user_id, video=my_video, caption=messanger_text)
                await asyncio.sleep(1)
            await asyncio.sleep(1)
            text_marker = False
            video_marker = False

        if video_marker:
            my_video = FSInputFile(messanger_video)
            for user in users:
                user_id = user[1]
                await bot.send_video(chat_id=user_id, video=my_video)
            await asyncio.sleep(1)

        if text_marker:
            for user in users:
                user_id = user[1]
                await bot.send_message(chat_id=user_id, text=f"{messanger_text}")
            await asyncio.sleep(1)


        if btns_marker:
            for user in users:
                user_id = user[1]
                await bot.send_message(chat_id=user_id, text=f"Так же подпишитесь на интересные каналы", reply_markup=channel_invite)
            await asyncio.sleep(1)

            await asyncio.sleep(2)
    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка не удалось отправить смс пользователю {user_id}  - {error}\n"
            error_file.write(error_message)
            print(error_message)

