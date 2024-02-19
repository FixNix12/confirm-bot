from aiogram import Bot
from aiogram.types import Message
from keyboards.main_keyboards import main_keyboards


async def get_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f' Дорогой администратор, \n'
                           f'вас приветствует бот по рассылки сообщений, \n'
                           f'здесь вы сможите настроить вашего бота \n\n\n',
                           reply_markup=main_keyboards)