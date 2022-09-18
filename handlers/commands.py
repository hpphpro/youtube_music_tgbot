from keyboard import menu_keyboard
from aiogram import types, Dispatcher
# from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove




async def start(message: types.Message):
    await message.answer('Select button below', reply_markup=menu_keyboard)


async def state_stop(message: types.Message):
    answer = message.text
    state = Dispatcher.get_current().current_state()
    if answer.lower() in ('/stop', 'stop'):
        await message.answer('If you want to start again -> enter /start', reply_markup=ReplyKeyboardRemove())
        return await state.finish()
    elif answer == '/start':
        await message.answer('Select button below', reply_markup=menu_keyboard)
        return await state.finish()


def handler_register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    
    