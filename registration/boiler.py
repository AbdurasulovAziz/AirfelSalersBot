from bot_create import dp, bot, LANGUAGE
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from database.db import SalerData
from keyboards import main_keyboard, sendAdmin_keyboard


class BoilerInfo(StatesGroup):
    photo = State()


class BoilerRegistration(BoilerInfo):

    async def start(message: types.Message, state: FSMContext):
        data = await state.get_data()
        await bot.send_message(chat_id=message.from_user.id, text=LANGUAGE[data['lang']]['SendSticker'],
                               reply_markup=types.ReplyKeyboardRemove())
        await BoilerInfo.photo.set()

    @dp.message_handler(content_types=types.ContentType.ANY, state=BoilerInfo.photo)
    async def __get_photo(message: types.Message, state: FSMContext):
        data = await state.get_data()
        if message.content_type == 'photo':
            saler_data = SalerData.get_user(message.from_user.id)
            caption = f"{LANGUAGE[data['lang']]['Saler']} {saler_data[1]}\n" \
                      f"{LANGUAGE[data['lang']]['SalerPhone']} {saler_data[2]}"
            await message.answer(LANGUAGE[data['lang']]['WaitPls'])
            await bot.send_photo('-1001552354835', message.photo[-1].file_id, caption=caption,
                                 reply_markup=await sendAdmin_keyboard(message.from_user.id, data["lang"]))
            await state.reset_state(with_data=False)
            await main_keyboard(message, state)
        else:
            await message.answer(f"{LANGUAGE[data['lang']]['SendSticker']}")
            await BoilerInfo.photo.set()

    @dp.callback_query_handler(regexp='(.+)-(.+)-(.+)')
    async def accept(call: types.CallbackQuery):
        callback = call.data.split('-')
        saler_data = SalerData.get_user(callback[1])
        caption = f'''{LANGUAGE['У́збекча']['Saler']} {saler_data[1]}\n{LANGUAGE['У́збекча']['SalerPhone']} {saler_data[2]}'''
        if callback[0] == 'Accept':
            SalerData.update_user_point(callback[1])
            await bot.send_message(chat_id=callback[1], text=LANGUAGE[callback[2]]['YourAccepted'])
            await call.message.edit_reply_markup(reply_markup=None)
            await call.message.edit_caption(f'{caption}\n{LANGUAGE["У́збекча"]["Accepted"]}')
        elif callback[0] == 'Decline':
            await bot.send_message(chat_id=callback[1], text=LANGUAGE[callback[2]]['YourDecline'])
            await call.message.edit_reply_markup(reply_markup=None)
            await call.message.edit_caption(f'{caption}\n{LANGUAGE["У́збекча"]["Declined"]}')
        await call.answer()
