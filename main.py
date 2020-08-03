import asyncio

from aiogram import executor
from load_all import bot
from keyboards import kbStart

from config import ADMIN_ID


async def on_startup(dp):
    await bot.send_message(ADMIN_ID, 'Я работаю!', reply_markup=kbStart)


async def on_shutdown(dp):
    await bot.close()


if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
