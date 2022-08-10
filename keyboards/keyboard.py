
from aiogram import types
from bot_create import LANGUAGE, bot
from aiogram.dispatcher import FSMContext




async def get_phone_keyboard(state:FSMContext):
    data = await state.get_data()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        types.KeyboardButton(LANGUAGE[data['lang']]['SendCon'], request_contact=True))
    return keyboard


async def main_keyboard(message: types.Message, state: FSMContext):
    data = await state.get_data()
    admin_id = await bot.get_chat_member(chat_id='-1001552354835', user_id=message.from_user.id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = [types.KeyboardButton(LANGUAGE[data['lang']]['RegCard']),
               types.KeyboardButton(LANGUAGE[data['lang']]['MyAccount']),
               types.KeyboardButton(LANGUAGE[data['lang']]['MyHistory']),
               types.KeyboardButton(LANGUAGE[data['lang']]['Prizes']),
               types.KeyboardButton(LANGUAGE[data['lang']]['ChangeLang'])]
    keyboard.add(*buttons)
    if admin_id['status'] != 'left':
        keyboard.add(types.KeyboardButton(LANGUAGE[data['lang']]['AdminPanel_keyboard']))
    await message.answer(LANGUAGE[data['lang']]['SelectNextDo'], reply_markup=keyboard)


async def sendAdmin_keyboard(master_id, master_lang):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=LANGUAGE['У́збекча']['Accept_keyboard'],
                                          callback_data=f'Accept-{master_id}-{master_lang}'),
               types.InlineKeyboardButton(text=LANGUAGE['У́збекча']['Decline_keyboard'],
                                          callback_data=f'Decline-{master_id}-{master_lang}')]
    keyboard.add(*buttons)
    return keyboard


async def admin_keyboard(state:FSMContext):
    data = await state.get_data()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(LANGUAGE[data['lang']]['GetData']),
               types.KeyboardButton(LANGUAGE[data['lang']]['GetHistory']),
               types.KeyboardButton(LANGUAGE[data['lang']]['Point_keyboard']),
               types.KeyboardButton('Сделать рассылку'),
               types.KeyboardButton(LANGUAGE[data['lang']]['Back'])]
    keyboard.add(*buttons)
    return keyboard

def language_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton('Русский'), types.KeyboardButton('У́збекча')]
    keyboard.add(*buttons)
    return keyboard

def history_keyboard(x,y):
    keyboard = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton('<<', callback_data=f'<<_{x}_{y}'),
               types.InlineKeyboardButton('>>', callback_data=f'>>_{x}_{y}')]
    keyboard.add(*buttons)
    return keyboard