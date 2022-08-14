from aiogram import types
# from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from markups import Button, menu_keyboard
# from create_bot import bot




async def continues(message: types.Message):
    if message.text == 'Yes':
        await message.answer('Select button below', reply_markup=menu_keyboard)
    elif message.text == 'No':
        await message.answer('Ok, goodluck!\nIf you want to start again tap -> /start', reply_markup=ReplyKeyboardRemove())


async def back_to_menu(message: types.Message):
    await message.answer('back', reply_markup=menu_keyboard)
 








def handler_register(dp):
    dp.register_message_handler(continues, Text(equals=Button.continuation_btns))
    dp.register_message_handler(back_to_menu, Text(equals=Button.back_to_menu))