import logging
import config

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage

logging.basicConfig(level=logging.INFO)

storage = RedisStorage(host='localhost', port=6379)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot, storage=storage)
