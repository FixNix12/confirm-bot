from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.sendler import MessengerState
from utils.database import Database
import os




async def add_text_messanger(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(message.from_user.id, f'Введите текст для рассылки')
    await state.set_state(MessengerState.mes_text)


async def handler_text_messanger(message: Message, bot: Bot, state: FSMContext):
    try:
        message_text = message.text

        await state.update_data(mes_text=message_text)

        data_id = 1

        data_state = await state.get_data()
        messanger_text = data_state.get('mes_text')

        db = Database(os.getenv('DATABASE_NAME'))
        text_status = db.add_or_update_messenger_text(data_id, messanger_text)

        await bot.send_message(message.from_user.id, f'Текст рассылки успешно добавлено')
        await state.clear()


    except Exception as error:
        with open('errors.txt', 'a') as error_file:
            error_message = f"Ошибка при записи текста рассылки - {error}\n"
            error_file.write(error_message)
            print(error_message)
