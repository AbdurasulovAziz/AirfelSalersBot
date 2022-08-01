from aiogram import executor
from bot_create import dp, bot, dotenv
from handlers import client

client.register_handlers_client(dp)

WEBHOOK_HOST = dotenv['WEBHOOK_HOST']
WEBHOOK_PATH = dotenv['WEBHOOK_PATH']
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = dotenv['WEBAPP_HOST']  # or ip
WEBAPP_PORT = dotenv['WEBAPP_PORT']


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()


executor.start_webhook(
    dispatcher=dp,
    webhook_path=WEBHOOK_PATH,
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host=WEBAPP_HOST,
    port=WEBAPP_PORT,
)
