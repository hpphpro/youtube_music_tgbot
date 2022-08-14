from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

import os

from markups import music_menu_keyboard, Button, music_choose_keyboard, continueation_keyboard
from parsers.converter import download, clear
from parsers.music import search
from utils import StateMachine as SM, Data
from create_bot import bot
from config import ROOT_DIR


async def music_menu(message: types.Message):
    await message.answer('Select button below', reply_markup=music_menu_keyboard)
  
async def search_by_title(message: types.Message):
    await message.answer('Enter a title that you want to find')
    await SM.music_by_title.set()

async def search_by_url(message: types.Message):
    await message.answer('Enter a youtube url.\nIf you want to drop your action -> enter <b>stop</b>')
    await SM.music_by_url.set()

async def download_by_url(message: types.Message, state: FSMContext):
    answer = message.text
    user_id = message.from_user.id
    if answer.lower() == 'stop':
        await message.answer('If you want to start again -> enter /start', reply_markup=ReplyKeyboardRemove())
        return await state.finish()

    if 'youtube.com' in answer or 'youtu.be' in answer:
        path = ROOT_DIR / str(user_id)
        await message.answer('Searching... it may take some time')
        download(url=answer, path=user_id)
        for name in os.listdir(path):
            if name.endswith('.mp3'):
                file = f'{path}/{name}'
                await bot.send_audio(message.chat.id, audio=open(file, 'rb'))
                break

        if os.path.exists(path):
            clear(path=path)

        await message.answer('Do you want to do something else?', reply_markup=continueation_keyboard)
        return await state.finish()
    else:
        await message.answer('Please enter youtube link')

async def get_music_by_title(message: types.Message, state: FSMContext):
    answer = message.text
    await message.answer('Searching...')
    if answer.lower() == 'stop':
        await message.answer('If you want to start again -> enter /start', reply_markup=ReplyKeyboardRemove())
        return await state.finish()
    track_list = await search(title=answer)
    index = 1
    for track in track_list:
        await message.answer(
            f'Track №{index}\n'
            f'{track}'
            )
        index += 1
    await message.answer('Choose what you want to download.\nIf you want to drop your action -> enter <b>stop</b>', reply_markup=music_choose_keyboard)
    Data.track_list = track_list
    await SM.music_by_titlev2.set()

async def download_by_choice(message: types.Message, state: FSMContext):
    answer = message.text
    if answer.lower() == 'stop':
        await message.answer('If you want to start again -> enter /start', reply_markup=ReplyKeyboardRemove())
        return await state.finish()
    user_id = message.from_user.id
    track_list_dict = Data.track_list
    track_list = tuple(track_list_dict)

    if answer not in Button.choose_btns:
        await message.answer('Choose button below.\nIf you want to drop your action -> enter <b>stop</b>', reply_markup=music_choose_keyboard)
    path = ROOT_DIR / str(user_id)
    try:
        await message.answer('Downloading... it may take some time')
        download(url=track_list[int(answer) - 1], path=user_id)
        for name in os.listdir(path):
            if name.endswith('.mp3'):
                os.rename(f'{path}/{name}', f'{path}/{track_list_dict[track_list[int(answer) - 1]]}.mp3')
                break
        file = f'{path}/{track_list_dict[track_list[int(answer) - 1]]}.mp3'
        await bot.send_audio(message.chat.id, audio=open(file, 'rb'))
    except Exception:
        if os.path.exists(path):
            clear(path=path)
        await message.answer('Got unexpected issue, to start again -> enter /start', reply_markup=ReplyKeyboardRemove())
        return await state.finish()

    Data.track_list = None
    if os.path.exists(path):
        clear(path=path)

    await message.answer('Do you want to do something else?', reply_markup=continueation_keyboard)
    return await state.finish()

def handler_register(dp):
    dp.register_message_handler(music_menu, Text(equals=Button.music_btn))
    dp.register_message_handler(search_by_title, Text(equals=Button.btn_search_title), state=None)
    dp.register_message_handler(get_music_by_title, state=SM.music_by_title)
    dp.register_message_handler(download_by_choice, state=SM.music_by_titlev2)
    dp.register_message_handler(search_by_url, Text(equals=Button.btn_search_url))
    dp.register_message_handler(download_by_url, state=SM.music_by_url)