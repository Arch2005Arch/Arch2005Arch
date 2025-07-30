import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage

from core.SETTINGS import settings
from core.handlers.basic import get_start
from core.handlers.paydostavka import shipping_check
from core.utils.commands import set_comands
from core.handlers.pay import successful_payment, pre_checkout_query, order
from core.handlers.paydostavka import handle_pre_checkout, handle_successful_payment, create_orders


async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен')



async def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

async def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )


    bot = Bot(
        token=settings.bots.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    await set_comands(bot)

    dp = Dispatcher(storage=MemoryStorage())

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_start, CommandStart())
    dp.message.register(order, Command(commands='pay'))
    dp.pre_checkout_query.register(pre_checkout_query)
    dp.message.register(successful_payment, F.successful_payment)

    dp.message.register(get_start, CommandStart())
    dp.message.register(create_orders, Command(commands='pay_dostavka'))
    dp.pre_checkout_query.register(handle_pre_checkout)
    dp.message.register(handle_successful_payment, F.successful_payment)
    dp.shipping_query.register(shipping_check)

    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Exit')
