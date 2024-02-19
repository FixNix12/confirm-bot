from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from state.video import VideoState
from utils.database import Database
import os
import random
import string


# создание кнопок с выбором канала
async def get_channels_key():
    db = Database(os.getenv('DATABASE_NAME'))
    channels = db.get_channels()

    inline_keyboard = []
    #
    for channel in channels:
        id_channel = channel[0]
        name_channel = channel[2]
        button = InlineKeyboardButton(text=name_channel, callback_data=f"video_channel_id:{id_channel}")  # Передает в параметры кнопки user_name в качестве информации вывода и user_id в качестве callback
        row = [button]
        inline_keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)





# Генератор случайного имени
def generate_short_name(length=5):
    characters = string.ascii_letters + string.digits  # Используются буквы и цифры
    return ''.join(random.choice(characters) for _ in range(length))


async def add_video(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, f'Прикрепите видео для приветствия')
    await state.set_state(VideoState.video_file)


async def handler_video(message: Message, bot: Bot, state: FSMContext):
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

        await state.update_data(video_file=video_file)

        keyboard = await get_channels_key()
        await bot.send_message(message.from_user.id, "Выберите канал за кем закрепить данныое видео:", reply_markup=keyboard)


    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при загрузке видео - {error}\n"
            error_file.write(error_message)
            print(error_message)


async def choice_channel_video(call: CallbackQuery, state: FSMContext):
    try:
        channel_id = int(call.data.split(":")[1])

        data_state = await state.get_data()
        video_file = data_state.get('video_file')


        db = Database(os.getenv('DATABASE_NAME'))
        video_status = db.add_or_update_greeting_video(channel_id, video_file)

        await call.message.answer(f'Видео успешно добавлено и закрепленно за каналом')
        await state.clear()

    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при попытке добавить запись видео в базу данных - {error}\n"
            error_file.write(error_message)
            print(error_message)