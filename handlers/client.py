from aiogram import Dispatcher, types
from aiogram.utils.exceptions import MessageTextIsEmpty
from bot_create import dp, LANGUAGE, bot
from registration import SalerRegistration, BoilerRegistration, Points, Language
from keyboards import main_keyboard, admin_keyboard, history_keyboard
from database import SalerData, AdminData
from aiogram.dispatcher import FSMContext
import pandas as pd


@dp.message_handler(commands='start')
async def start(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        saler_data = SalerData.get_user(message.from_user.id)
        if saler_data is None:
            await SalerRegistration.start(message)
        else:
            try:
                await message.answer(LANGUAGE[data['lang']]['SelectNextDo'])
                await main_keyboard(message, state)
            except KeyError:
                await SalerRegistration.start(message)
    except TypeError:
        await message.answer('Бот уже запущен')
        await main_keyboard(message, state)


@dp.message_handler(lambda message: message.text == 'Менинг анкетам👨🏻‍💼' or message.text == 'Моя анкета👨🏻‍💼')
async def get_info(message: types.Message, state: FSMContext):
    data = await state.get_data()
    master = SalerData.get_user(message.from_user.id)
    text = f'''{LANGUAGE[data['lang']]['Name']} {master[1]}\n{LANGUAGE[data['lang']]['Phone']} {master[2]}\n{LANGUAGE[data['lang']]['Points']} {master[3]}'''
    await message.answer(text)

@dp.message_handler(lambda message: message.text == 'Моя история' or message.text == 'Менинг тарихим')
async def get_history(message: types.Message, state: FSMContext):
    data = await state.get_data()
    saler_history = SalerData.get_history(message.from_user.id)
    try:
        x, y = 0, 5
        keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('>>', callback_data=f'>>_{x}_{y}'))
        if len(saler_history) <= y:
            await message.answer(list_to_text(x, y, saler_history))
        else:
            await message.answer(list_to_text(x, y, saler_history), reply_markup=keyboard)
    except MessageTextIsEmpty:
        await message.answer(LANGUAGE[data['lang']]['EmptyHistory'])

    @dp.callback_query_handler(regexp=('(.+)_(.+)_(.+)'))
    async def histor(call: types.CallbackQuery):

        saler_history = SalerData.get_history(message.from_user.id)
        callback = []

        for i in call.data.split('_'):
            try:
                callback.append(int(i))
            except ValueError:
                callback.append(i)

        if callback[0] == '>>':
            callback[1] += 5
            callback[2] += 5

            if callback[2] >= len(saler_history):
                keyboard = types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton('<<', callback_data=f'<<_{callback[1]}_{callback[2]}'))
                await call.message.edit_text(
                    list_to_text(callback[2]-5, len(saler_history), saler_history), reply_markup=keyboard)
            else:
                await call.message.edit_text(
                    list_to_text(
                        callback[1], callback[2], saler_history), reply_markup=history_keyboard(callback[1], callback[2]))

        elif callback[0] == '<<':

            if (callback[1]-5) <= 0:
                callback[1], callback[2] = 0, 5
                keyboard = types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton('>>', callback_data=f'>>_{callback[1]}_{callback[2]}'))
                await call.message.edit_text(
                    list_to_text(callback[1], callback[2], saler_history), reply_markup=keyboard)
            else:
                callback[1] -= 5
                callback[2] -= 5
                await call.message.edit_text(
                    list_to_text(callback[1], callback[2], saler_history),
                    reply_markup=history_keyboard(callback[1], callback[2])
                )

        await call.answer()


@dp.message_handler(lambda message: message.text == 'Карточканинг суратини жўнатинг' or
                                    message.text == 'Отправить фотографию карточки')
async def send_photo(message: types.Message, state: FSMContext):
    await BoilerRegistration.start(message, state)


@dp.message_handler(lambda message: message.text == 'Призы' or message.text == 'Совринлар')
async def get_prizes(message: types.Message):
    photo = open('images/image.png', 'rb')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)


@dp.message_handler(lambda message: message.text == 'Администратор бўлими' or message.text == 'Админ панель')
async def get_data(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(LANGUAGE[data['lang']]['AdminPanel'], reply_markup=await admin_keyboard(state))

    @dp.message_handler(lambda message: message.text == 'Маълумотларни юклаш' or message.text == 'Получить данные')
    async def get_excel(message: types.Message):
        saler_data = AdminData.get_excel()
        columns = ['Name', 'Phone', 'Points']
        array = []
        for i in saler_data:
            arr = []
            for j in i:
                arr.append(j)
            array.append(arr)
        array = pd.DataFrame(array, columns=columns)
        array.to_excel('database/Маълумотлар.xlsx', index=False)
        await message.reply_document(open('database/Маълумотлар.xlsx', 'rb'))

    @dp.message_handler(lambda message: message.text == 'Баллы' or message.text == 'Баллар')
    async def minusPoint(message: types.Message, state: FSMContext):
        await Points.take_points(message, state)

    @dp.message_handler(lambda message: message.text == 'Получить историю' or message.text == 'Тарихни кўриш')
    async def get_history(message: types.Message):
        history_data = AdminData.get_history()
        columns = ['Name', 'Phone', 'Time', 'Points']
        array = []
        for i in history_data:
            arr = []
            for j in i:
                arr.append(str(j))
            array.append(arr)
        array = pd.DataFrame(array, columns=columns)
        array.to_excel('database/Tarix.xlsx', index=False)
        await message.reply_document(open('database/Tarix.xlsx', 'rb'))

    @dp.message_handler(lambda message: message.text == 'Ортга қайтиш⬅️' or message.text == 'Назад⬅️')
    async def get_back(message: types.Message, state: FSMContext):
        await main_keyboard(message, state)


@dp.message_handler(lambda message: message.text == 'Поменять язык' or message.text == 'Тилни ўзгартириш')
async def change_lang(message: types.Message):
    await Language.change_language(message)




def list_to_text(x, y, list):
    new_list = list[x:y]
    text = ''
    for i in new_list:
        text += i + '\n'
    return text




def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
