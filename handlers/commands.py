from markups import menu_keyboard
from aiogram import types
# from aiogram.types import ReplyKeyboardRemove



async def start(message: types.Message):
    await message.answer('Select button below', reply_markup=menu_keyboard)



def handler_register(dp):
    dp.register_message_handler(start, commands=['start'])
    