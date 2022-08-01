from aiogram import executor
from bot_create import dp
from handlers import client


client.register_handlers_client(dp)
executor.start_polling(dp, skip_updates=True)