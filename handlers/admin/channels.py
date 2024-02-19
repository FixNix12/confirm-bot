from aiogram.types import Message
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from state.channels import ChannelsState
from utils.database import Database
import os
import re
import asyncio
from keyboards.channels import channels_keyboards


async def view_channels_commands(messgae: Message, bot: Bot):
    await bot.send_message(messgae.from_user.id, f"Выберите действие с каналом", reply_markup=channels_keyboards)


async def add_channels(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, f"Пожалуйста  введите channel_id канала\n\n"
                                                 f"*Узнать можно переотправив СМС от канала в @raw_data_bot")
    await state.set_state(ChannelsState.channel_id)



async def add_channel_id(message: Message, bot: Bot, state: FSMContext):
    user_message = message.text

    if(re.findall("^-\\d+$", message.text)):

        try:
            await state.update_data(channel_id=user_message)
            await bot.send_message(message.from_user.id, f"{user_message} - добавлен как chat_id")
            await asyncio.sleep(2)
            await bot.send_message(message.from_user.id, f"Теперь введите название вашего канала")
            await state.set_state(ChannelsState.channel_name)

        except Exception as error:
            with open('errors.txt', 'a') as error_file:
                error_message = f"Ошибка при попытке записать channel_id в состояние - {error}\n"
                error_file.write(error_message)
                print(error_message)
    else:
        await bot.send_message(message.from_user.id, f"Введенный текст не соответствует формату channel_id. Пожалуйста, введите корректный channel_id, начинающийся с '-' и состоящий только из цифр.")



async def add_channel_name(message: Message, bot: Bot, state: FSMContext):
    channel_name = message.text
    try:
        await state.update_data(channel_name=message.text)
        await bot.send_message(message.from_user.id, f'{channel_name} - добавлен как название канала\n'
                                                     f'Последний шаг регистрации: введите пригласительную ссылку на ваш канал')
        await state.set_state(ChannelsState.channel_link)

    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при попытке записать channel_name в состояние - {error}\n"
            error_file.write(error_message)
            print(error_message)



async def add_channel_link(message: Message, bot: Bot, state: FSMContext):
    channel_link = message.text
    if(re.findall(r"^https:\/\/t\.me\/", channel_link)):
        try:
            db = Database(os.getenv('DATABASE_NAME'))
            await state.update_data(channel_link=message.text)
            channel_data = await state.get_data()
            channel_id = channel_data.get('channel_id')
            channel_name = channel_data.get('channel_name')
            channel_link = channel_data.get('channel_link')

            create_channel = db.add_channels(channel_id, channel_name, channel_link)

            await bot.send_message(message.from_user.id, f"Канал успешно добавлен")
            await state.clear()

        except Exception as error:
            with open('errors.txt', 'a') as error_file:
                error_message = f"Ошибка при попытке создать запись канала - {error}\n"
                error_file.write(error_message)
                print(error_message)
    else:
        await bot.send_message(message.from_user.id, f'Неверный формат ссыллки !\n'
                                                     f'Ссылка должна начинаться с: https://t.me/')