from  aiogram.filters import BaseFilter
from aiogram.types import Message
import os



class CheckAdmin(BaseFilter):
    async def __call__(self, message: Message):
        admins_ids_str = os.getenv('ADMINS_ID') # получение списка администраторов которым разрешено пользоваться ботом с файла env
        admins_ids_list = admins_ids_str.replace('[', '').replace(']', '').replace(' ', '').split(',')
        admins_ids = list(map(int, admins_ids_list))
        user_id = message.from_user.id  # Получаем ID пользователя из сообщения
        if user_id in admins_ids:
            return True
        else:
            await message.reply("Только администраторы имеют возможность пользоваться данным ботом !")
            return False