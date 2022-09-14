from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from dotenv import dotenv_values
from languages import BOT_LANGUAGE
dotenv = dict(dotenv_values('.env'))

storage = MemoryStorage()

admin_chat = -1001552354835

LANGUAGE=BOT_LANGUAGE


bot = Bot(token=dotenv['BOT_TOKEN'], parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)



