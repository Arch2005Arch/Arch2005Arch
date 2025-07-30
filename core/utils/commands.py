from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault



async def set_comands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало роботы'
        ),
        BotCommand(
            command='pay',
            description='Оплата'
        ),
        BotCommand(
            command='pay_dostavka',
            description='Оплата матирального продукта с доставкой'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())