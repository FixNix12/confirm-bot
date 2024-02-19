from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from state.button import BtnState
from utils.database import Database
import os
import re


# создание кнопок с выбором канала
async def get_channels_key():
    db = Database(os.getenv('DATABASE_NAME'))
    channels = db.get_channels()

    inline_keyboard = []
    #
    for channel in channels:
        id_channel = channel[0]
        name_channel = channel[2]
        button = InlineKeyboardButton(text=name_channel, callback_data=f"btn_channel_id:{id_channel}")  # Передает в параметры кнопки user_name в качестве информации вывода и user_id в качестве callback
        row = [button]
        inline_keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)




async def add_btns_text(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, f'Введите текст для кнопки')
    await state.set_state(BtnState.btn_text)


async def add_btns_link(message: Message, bot: Bot, state: FSMContext):
    try:
        btn_text = message.text
        await state.update_data(btn_text=btn_text)
        await bot.send_message(message.from_user.id, f'Введите ссылку для кнопки')
        await state.set_state(BtnState.btn_link)
    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при записи текста кнопки в состояние - {error}\n"
            error_file.write(error_message)
            print(error_message)


async def handler_btn(message: Message, bot: Bot, state: FSMContext):
    btn_link = message.text
    if (re.findall(r"^(https?://)", btn_link)):
        try:


            await state.update_data(btn_link=btn_link)

            keyboard = await get_channels_key()
            await bot.send_message(message.from_user.id, "Выберите канал за кем закрепить данные кнопки:", reply_markup=keyboard)

        except Exception as error:
            with open('errors.txt', 'a') as error_file:
                error_message = f"Ошибка при записи текста ссылки кнопки в состояние - {error}\n"
                error_file.write(error_message)
                print(error_message)
    else:
        await bot.send_message(message.from_user.id, f'Неверный формат ссыллки !\n'

                                                     f'Ссылка должна начинаться с: "https://" или "http://"')


async def choice_channel_btn(call: CallbackQuery, state: FSMContext):
    try:
        channel_id = int(call.data.split(":")[1])

        data_state = await state.get_data()
        btn_text = data_state.get('btn_text')
        btn_link = data_state.get('btn_link')


        db = Database(os.getenv('DATABASE_NAME'))
        btn_status = db.add_or_update_greeting_btn(channel_id, btn_text, btn_link)

        await call.message.answer(f'Кнопка успешно добавлено и закрепленно за каналом')

        await state.clear()

    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при попытке добавить кнопек для канала в базу данных - {error}\n"
            error_file.write(error_message)
            print(error_message)