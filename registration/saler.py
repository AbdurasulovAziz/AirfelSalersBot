from bot_create import dp, LANGUAGE
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from database import SalerData
from keyboards import get_phone_keyboard, main_keyboard, language_keyboard


class SalerInfo(StatesGroup):
    language = State()
    username = State()
    phone = State()


class SalerRegistration(SalerInfo):

    async def start(message: types.Message):
        await message.answer('Выберите язык:\nТилни танланг:', reply_markup=language_keyboard())
        await SalerInfo.language.set()

    @dp.message_handler(state=SalerInfo.language)
    async def __get_lang(message: types.Message, state: FSMContext):
        if message.text in ['Русский', 'У́збекча']:
            await state.update_data(lang=message.text)
            if True:
                await message.answer(LANGUAGE[message.text]['SendName'], reply_markup=types.ReplyKeyboardRemove())
            await SalerInfo.username.set()
        else:
            await message.answer('Выберите на клавиатуре\nKlaviaturadan tanlang')
            await SalerInfo.language.set()

    @dp.message_handler(state=SalerInfo.username)
    async def __get_username(message: types.Message, state: FSMContext):
        data = await state.get_data()
        if len(message.text.split()) == 2:
            await state.update_data(saler_fio=message.text)
            await message.answer(LANGUAGE[data['lang']]['SendPhone_keyboard'],
                                 reply_markup=await get_phone_keyboard(state))
            await SalerInfo.phone.set()
        else:
            await message.answer(LANGUAGE[data['lang']]['TryAgain'])
            await SalerInfo.username.set()

    @dp.message_handler(content_types='contact', state=SalerInfo.phone)
    async def __get_phone(message: types.Message, state: FSMContext):
        await state.update_data(saler_phone=message['contact']['phone_number'],
                                saler_id=message['contact']['user_id'])
        saler = SalerData.get_user(message.from_user.id)
        data = await state.get_data()
        if saler is None:
            SalerData.add_user(data['saler_id'], data['saler_fio'], data['saler_phone'])
            await message.answer(LANGUAGE[data['lang']]['AccountCreated'],
                                 reply_markup=types.ReplyKeyboardRemove())
        else:
            SalerData.update_user(data['saler_id'],
                                  data['saler_fio'],
                                  data['saler_phone'])
            await message.answer(LANGUAGE[data['lang']]['AccountUpdated'],
                                 reply_markup=types.ReplyKeyboardRemove())
        await state.reset_state(with_data=False)
        await main_keyboard(message, state)
