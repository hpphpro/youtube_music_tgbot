from keyboard import menu_keyboard
from aiogram import types, Dispatcher
# from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove




async def start(message: types.Message):
    await message.answer('Select button below', reply_markup=menu_keyboard)


async def state_stop(message: types.Message):
    state = Dispatcher.get_current().current_state()
    await message.answer('If you want to start again -> enter /start', reply_markup=ReplyKeyboardRemove())
    return await state.finish()
    


async def handler_register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(state_stop, commands=['stop', 'cancel'], state='*')
    
    