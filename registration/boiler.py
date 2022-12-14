from bot_create import dp, bot, LANGUAGE, admin_chat
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from database.db import SalerData
from keyboards import main_keyboard, sendAdmin_keyboard
import yadisk
from datetime import datetime, timedelta
import os

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
            await bot.send_photo(admin_chat, message.photo[-1].file_id, caption=caption,
                                 reply_markup=await sendAdmin_keyboard(message.from_user.id, data["lang"]))
            await state.reset_state(with_data=False)
            await main_keyboard(message, state)
        else:
            await message.answer(f"{LANGUAGE[data['lang']]['SendSticker']}")
            await BoilerInfo.photo.set()

    @dp.callback_query_handler(regexp='(.+)-(.+)-(.+)')
    async def accept(call: types.CallbackQuery):
        y = yadisk.YaDisk(token='y0_AgAAAABkRiIFAAhhOQAAAADNxaUa5HggKsNbTYSdpfFYiKjje1KR5O4')
        callback = call.data.split('-')
        saler_data = SalerData.get_user(callback[1])
        caption = f'''{LANGUAGE['У́збекча']['Saler']} {saler_data[1]}\n{LANGUAGE['У́збекча']['SalerPhone']} {saler_data[2]}'''
        if callback[0] == 'Accept':
            await call.message.edit_reply_markup(reply_markup=None)

            imgname = f'{(datetime.now() + timedelta(hours=3)).strftime("%Y_%m_%d %H_%M_%S")} {saler_data[2]}.png'
            await call.message.photo[-1].download(f'registration/yadiskIMG/{imgname}')


            with open(f'registration/yadiskIMG/{imgname}', 'rb') as image:
                y.upload(image, f'/AirfelSavdo/{imgname}')
            os.remove(f'registration/yadiskIMG/{imgname}')

            SalerData.update_user_point(callback[1])

            await call.message.edit_caption(f'{caption}\n{LANGUAGE["У́збекча"]["Accepted"]}')
            await bot.send_message(chat_id=callback[1], text=LANGUAGE[callback[2]]['YourAccepted'])
        elif callback[0] == 'Decline':
            await bot.send_message(chat_id=callback[1], text=LANGUAGE[callback[2]]['YourDecline'])
            await call.message.edit_reply_markup(reply_markup=None)
            await call.message.edit_caption(f'{caption}\n{LANGUAGE["У́збекча"]["Declined"]}')
        await call.answer()


