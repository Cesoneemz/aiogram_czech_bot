from aiogram import types
from aiogram.dispatcher import FSMContext

from config import ADMIN_ID
from load_all import dp, bot
from keyboards import adminKeyboard


@dp.message_handler(user_id=ADMIN_ID, commands=['/admin'])
async def send_admin_panel(message: types.Message):
    await message.answer("Вхожу в админ-панель", reply_markup=adminKeyboard)


@dp.message_handler(user_id=ADMIN_ID, commands='/ban', lambda msg: msg.text.lower() == 'забанить пользователя')
async def ban_user(message: types.Message):

