import contextlib

from aiogram import Bot, Dispatcher, F
import asyncio
import logging
from dotenv import load_dotenv
import os
from aiogram.filters import Command
from handlers.joinuser import approve_request, approve_user, object_message
from handlers.admin.messenger import start_create, create_mailing, mailing_list_launch
from utils.database import Database
from state.sendler import Messenger
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





# Вызовы handlers


# Вывод объекта message
dp.message.register(object_message, Command(commands='message'))
dp.chat_join_request.register(approve_request)

# Обработка капчи
dp.message.register(approve_user, F.text == '🦊')
dp.message.register(approve_user, F.text == '🐻')
dp.message.register(approve_user, F.text == '🦁')

# Рассылка
dp.message.register(start_create, Command(commands='messanger'), CheckAdmin())
dp.message.register(create_mailing, Messenger.messtext)

#Запуск рассылки
dp.message.register(mailing_list_launch, Command(commands='starter'), CheckAdmin())




async def start():
    await set_commands(bot)
    db = Database(os.getenv('DATABASE_NAME'))
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())



