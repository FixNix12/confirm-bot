from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Запускаем Бота'
        ),
        BotCommand(
            command='messanger',
            description='Команда для старта записи нового сообщения'
        ),
        BotCommand(
            command='starter',
            description='Команда для запуска рассылки'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())