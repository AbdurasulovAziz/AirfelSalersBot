from bot_create import dp, LANGUAGE, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from database import SalerData
from keyboards.keyboard import main_keyboard

class Mail_Status(StatesGroup):
    message = State()

class Mail(Mail_Status):

    @staticmethod
    async def mail_start(message: types.Message, state:FSMContext):
        data = await state.get_data()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton(LANGUAGE[data['lang']]['Back']))
        await message.answer(LANGUAGE[data['lang']]['SendMess'], reply_markup=keyboard)
        await Mail_Status.message.set()

    @dp.message_handler(state=Mail_Status.message)
    async def __mailling(message:types.Message, state: FSMContext):
        data = await state.get_data()
        if message.text == (LANGUAGE[data['lang']]['Back']):
            await state.reset_state(with_data=False)
            await main_keyboard(message, state)
        else:
            users_id = SalerData.get_users_id()
            for user_id in users_id:
                user = list(user_id)[0]
                await bot.send_message(user, message.text)
            await state.reset_state(with_data=False)
            await main_keyboard(message, state)

