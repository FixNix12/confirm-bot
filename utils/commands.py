from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Запускаем Бота'
        ),
        BotCommand(
            command='mainmenu',
            description='Команда откроет основное меню управления'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())