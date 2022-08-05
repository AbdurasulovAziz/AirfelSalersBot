from bot_create import dp, LANGUAGE
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from database import SalerData
from database.db import AdminData
from keyboards.keyboard import main_keyboard


class SalerPoint(StatesGroup):

    phone = State()
    plus_or_minus = State()
    points = State()


class Points(SalerPoint):

    async def take_points(message: types.Message, state: FSMContext):
        data = await state.get_data()
        await message.answer(LANGUAGE[data['lang']]['SalerNum'], reply_markup=types.ReplyKeyboardRemove())
        await SalerPoint.phone.set()

    @dp.message_handler(state=SalerPoint.phone)
    async def __get_master_phone(message: types.Message, state: FSMContext):
        saler_data = AdminData.get_user_data(message.text)
        data = await state.get_data()
        if saler_data is not None:
            await state.update_data(saler_phone=message.text)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [types.KeyboardButton(LANGUAGE[data['lang']]['PlusPoint']),
                       types.KeyboardButton(LANGUAGE[data['lang']]['MinusPoint'])]
            keyboard.add(*buttons)
            await message.answer(LANGUAGE[data['lang']]['SelectNextDo'], reply_markup=keyboard)
            await SalerPoint.plus_or_minus.set()
        else:
            await message.answer(LANGUAGE[data['lang']]['NoTel'])
            await SalerPoint.phone.set()

    @dp.message_handler(state=SalerPoint.plus_or_minus)
    async def __plus_or_minus(message:types.Message, state:FSMContext):
        data = await state.get_data()
        if message.text == LANGUAGE[data['lang']]['PlusPoint']:
            await state.update_data(plus_or_minus='plus')
            await message.answer(LANGUAGE[data['lang']]['SendPoints'], reply_markup=types.ReplyKeyboardRemove())
            await SalerPoint.points.set()
        elif message.text == LANGUAGE[data['lang']]['MinusPoint']:
            await state.update_data(plus_or_minus='minus')
            await message.answer(LANGUAGE[data['lang']]['SendPoints'], reply_markup=types.ReplyKeyboardRemove())
            await SalerPoint.points.set()
        else:
            await message.answer(LANGUAGE[data['lang']]['TryAgain'])


    @dp.message_handler(state=SalerPoint.points)
    async def __get_points(message:types.Message, state: FSMContext):
        if message.text.isdigit():
            await state.update_data(points=int(message.text))
            data = await state.get_data()
            if data['plus_or_minus'] == 'plus':
                SalerData.plus_user_point(data['saler_phone'], data['points'])
            elif data['plus_or_minus'] == 'minus':
                SalerData.minus_user_point(data['saler_phone'], data['points'])
            await message.answer(LANGUAGE[data['lang']]['SalerUpdated'])
            await main_keyboard(message, state)
            await state.reset_state(with_data=False)
        else:
            data = await state.get_data()
            await message.answer(LANGUAGE[data['lang']]['SendDig'])
            await SalerPoint.points.set()
