from bot_create import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards import main_keyboard, language_keyboard




class LanguageInfo(StatesGroup):
    language = State()

class Language(LanguageInfo):

    async def change_language(message: types.Message):
        await message.answer('Выберите язык:\nТилни танланг:', reply_markup=language_keyboard())
        await LanguageInfo.language.set()

        @dp.message_handler(state=LanguageInfo.language)
        async def __leng(message: types.Message, state: FSMContext):

            if message.text in ['Русский', 'У́збекча']:
                await state.update_data(lang=message.text)
                await main_keyboard(message, state)
                await state.reset_state(with_data=False)
            else:
                await message.answer('Выберите на клавиатуре\nklaviaturadan tanlang')
                await LanguageInfo.language.set()