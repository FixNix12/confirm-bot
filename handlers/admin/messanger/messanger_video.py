from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.sendler import MessengerVideoState
from utils.database import Database
import os
import random
import string




# Генератор случайного имени
def generate_short_name(length=5):
    characters = string.ascii_letters + string.digits  # Используются буквы и цифры
    return ''.join(random.choice(characters) for _ in range(length))


async def add_video_messanger(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, f'Прикрепите видео для рассылки')
    await state.set_state(MessengerVideoState.mes_video_text)


async def handler_video_messanger(message: Message, bot: Bot, state: FSMContext):
    try:
        video_file_id = message.video.file_id
        video_name = generate_short_name() + '.mp4'
        file = await bot.get_file(video_file_id)
        file_path = file.file_path

        save_directory = './media/videos/'
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        await bot.download_file(file_path, os.path.join(save_directory, video_name))

        video_file = f'{save_directory}{video_name}'

        print(video_file)

        data_id = 1

        db = Database(os.getenv('DATABASE_NAME'))
        video_status = db.add_or_update_messenger_video(data_id, video_file)

        await bot.send_message(message.from_user.id, f'Видео успешно добавлено и закрепленно за каналом')
        await state.clear()


    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при загрузке видео - {error}\n"
            error_file.write(error_message)
            print(error_message)