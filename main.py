import contextlib

from aiogram import Bot, Dispatcher, F
import asyncio
import logging
from dotenv import load_dotenv
import os
from aiogram.types import Message
from aiogram.filters import Command


from handlers.joinuser import approve_request, approve_user, object_message
from handlers.admin.channels import view_channels_commands, add_channels, add_channel_id, add_channel_name, add_channel_link
from handlers.admin.greeting_video import handler_video, add_video, choice_channel_video
from handlers.admin.greeting_text import handler_text, add_text, choice_channel_text
from handlers.admin.greeting_btn import add_btns_text, add_btns_link, handler_btn, choice_channel_btn
from keyboards.main_keyboards import main_keyboards, greeting_keyboards, channels_keyboards, messager_keyboards, delete_keyboards
from handlers.admin.messanger.messanger_text import add_text_messanger, handler_text_messanger
from handlers.admin.messanger.messanger_video import  add_video_messanger, handler_video_messanger
from handlers.admin.messanger.start_messanger import mailing_list_launch
from handlers.admin.delete.delete_data import delete_channel, try_delete_channel, delete_greeting, try_delete_greeting, delete_messanger

from utils.database import Database


from state.channels import ChannelsState
from state.video import VideoState
from state.text import TextState
from state.button import BtnState
from state.sendler import MessengerState, MessengerVideoState

from filters.CheckAdmin import CheckAdmin
from utils.commands import set_commands

load_dotenv()

#загрузка данных и файла env (для безопасности)
load_dotenv()

#получение токена используемого бота
token = os.getenv('BOT_TOKEN')

#chat_id главного администратора для дальнейшего уведомления
admin_id = os.getenv('ADMIN_ID')

#экземпляр бота
bot = Bot(token=token, parse_mode='HTML')

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

#объявление диспетчера
dp = Dispatcher()


CHANNEL_ID = -1002096606551

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")


# Меню
async def view_main_menu(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f"Основное меню", reply_markup=main_keyboards)

dp.message.register(view_main_menu, Command(commands='mainmenu'))
@dp.message(F.text=='Основное меню',  CheckAdmin()) # вызов функции показа основного меню
async def main_menu(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id,f"Основное меню", reply_markup=main_keyboards)

@dp.message(F.text=="Управление приветствием", CheckAdmin())
async def replace_message(message: Message, bot: Bot):
        await bot.send_message(message.from_user.id,"Выберите действие с аккаунтом", reply_markup=greeting_keyboards)

@dp.message(F.text=="Управление каналами", CheckAdmin())
async def replace_message(message: Message, bot: Bot):
        await bot.send_message(message.from_user.id,"Выберите действие с каналом", reply_markup=channels_keyboards)

@dp.message(F.text=="Управление рассылкой", CheckAdmin())
async def replace_message(message: Message, bot: Bot):
        await bot.send_message(message.from_user.id,"Выберите действие с рассылкой", reply_markup=messager_keyboards)

@dp.message(F.text=="Удаление метериала", CheckAdmin())
async def replace_message(message: Message, bot: Bot):
        await bot.send_message(message.from_user.id,"Выберите материал для удаления", reply_markup=delete_keyboards)



# Вызовы handlers


# Вывод объекта message
dp.message.register(object_message, Command(commands='message'))
dp.chat_join_request.register(approve_request)

# Обработка капчи
dp.message.register(approve_user, F.text == '🦊')
dp.message.register(approve_user, F.text == '🐻')
dp.message.register(approve_user, F.text == '🦁')

# Рассылка
dp.message.register(add_text_messanger, F.text == 'Добавить тект рассылки', CheckAdmin())
dp.message.register(handler_text_messanger, MessengerState.mes_text, CheckAdmin())

dp.message.register(add_video_messanger, F.text == 'Добавить видео рассылки', CheckAdmin())
dp.message.register(handler_video_messanger, MessengerVideoState.mes_video_text, CheckAdmin())

dp.message.register(handler_video_messanger, MessengerVideoState.mes_video_text, CheckAdmin())
dp.message.register(mailing_list_launch, F.text == 'Запустить рассылку', CheckAdmin())

# Работа с каналами
dp.message.register(view_channels_commands, Command(commands='channels'), CheckAdmin())
dp.message.register(add_channels, F.text == "Добавить канал", CheckAdmin())
dp.message.register(add_channel_id, ChannelsState.channel_id, CheckAdmin())
dp.message.register(add_channel_name, ChannelsState.channel_name, CheckAdmin())
dp.message.register(add_channel_link, ChannelsState.channel_link, CheckAdmin())

# Работа с видео приветствия
dp.message.register(add_video, F.text == "Добавить видео приветствия")
dp.message.register(handler_video, VideoState.video_file)
dp.callback_query.register(choice_channel_video, lambda c: c.data.startswith('video_channel_id'))

# Работа с текстом приветствия
dp.message.register(add_text, F.text == "Добавить тект приветствия")
dp.message.register(handler_text, TextState.text_message)
dp.callback_query.register(choice_channel_text, lambda c: c.data.startswith('text_channel_id'))

# Работа с кнопками приветствия
dp.message.register(add_btns_text, F.text == "Добавить кнопку приветствия")
dp.message.register(add_btns_link, BtnState.btn_text)
dp.message.register(handler_btn, BtnState.btn_link)
dp.callback_query.register(choice_channel_btn, lambda c: c.data.startswith('btn_channel_id'))


# Фаза удаления
dp.message.register(delete_channel, F.text == "Удалить канал")
dp.callback_query.register(try_delete_channel, lambda c: c.data.startswith('delete_channel'))
dp.message.register(delete_greeting, F.text == "Удалить приветствие")
dp.callback_query.register(try_delete_greeting, lambda c: c.data.startswith('delete_greeting'))
dp.message.register(delete_messanger, F.text == "Удалить рассылку")



async def start():
    await set_commands(bot)
    db = Database(os.getenv('DATABASE_NAME'))
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())



