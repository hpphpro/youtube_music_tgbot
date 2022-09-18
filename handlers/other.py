from aiogram import types, Dispatcher
# from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from keyboard import menu_keyboard
# from create_bot import bot




async def continues(message: types.Message):
    if message.text == 'Yes':
        await message.answer('Select button below', reply_markup=menu_keyboard)
    elif message.text == 'No':
        await message.answer('Ok, goodluck!\nIf you want to start again tap -> /start', reply_markup=ReplyKeyboardRemove())


async def back_to_menu(message: types.Message):
    await message.answer('back', reply_markup=menu_keyboard)
 





def handler_register(dp: Dispatcher) -> None:
    dp.register_message_handler(continues, Text(equals=('Yes', 'No')))
    dp.register_message_handler(back_to_menu, Text(equals='back'))