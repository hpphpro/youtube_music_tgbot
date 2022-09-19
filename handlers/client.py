from cmath import inf
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

import os

from keyboard import music_menu_keyboard, continuation_keyboard
from keyboard.inline import inline_button
from parsers import download, clear, search
from utils import StateMachine
from loader import bot
from config import ROOT_DIR
from utils.logger import info



async def music_menu(message: types.Message):
    
    await message.answer('Select button below', reply_markup=music_menu_keyboard)
  
  
async def search_by_title(message: types.Message):
    
    await message.answer('Enter a title that you want to find', reply_markup=ReplyKeyboardRemove())
    await StateMachine.music_by_title.set()


async def search_by_url(message: types.Message):
    
    await message.answer('Enter a youtube url.\nIf you want to drop your action -> enter <b>/stop</b>', reply_markup=ReplyKeyboardRemove())
    await StateMachine.music_by_url.set()


async def download_by_url(message: types.Message, state: FSMContext):
    
    answer = message.text
    user_id = str(message.from_user.id)
    message_type: list[dict] = message.entities
    
    if answer in ('/stop', '/cancel'):
        await message.answer('If you want to start again -> enter /start', reply_markup=ReplyKeyboardRemove())
        return await state.finish()
    
    if message_type and [True for d in message_type if d['type'] == 'url']\
        and 'youtube.com' in answer or 'youtu.be' in answer:
            
        path = ROOT_DIR / user_id
        try:
            await message.answer('Searching... it may take some time', reply_markup=ReplyKeyboardRemove())
            await download(url=answer, path=user_id)
            for name in os.listdir(path):
                if name.endswith('.mp3'):
                    file = f'{path}/{name}'
                    await bot.send_audio(message.chat.id, audio=open(file, 'rb'), title=f'{name}.mp3')
                    break
        except Exception as ex:
            info(ex)
            await message.answer('Got unexpected issue, to start again -> enter /start', reply_markup=ReplyKeyboardRemove())
            return await state.finish()
        else:
            await message.answer('Do you want to do something else?', reply_markup=continuation_keyboard)
            return await state.finish()
        finally:
            if os.path.exists(path):
                await clear(path=path)
    else:
        await message.answer('Please enter youtube link')


async def get_music_by_title(message: types.Message, state: FSMContext):
    
    answer = message.text
    message_type: list[dict] = message.entities

    if answer in ('/stop', '/cancel'):
        await message.answer('If you want to start again -> enter /start', reply_markup=ReplyKeyboardRemove())
        return await state.finish()
    
    if message_type and [True for d in message_type if d['type'] == 'url']:
        await message.answer('Enter a title please, not link')    
    else:
        track_list = await search(title=answer)
        
        
        choose_message_id = []
        for index, track in enumerate(track_list, start=1):
            msg = await message.answer(
                f'Track №{index}\n{track}',
                reply_markup=inline_button(text='Download', callback=index)
                )
            choose_message_id.append(msg.message_id)
    
        msg = await message.answer('Choose what you want to download.\nIf you want to drop your action -> enter <b>/stop</b>')
        choose_message_id.append(msg.message_id)
        
        async with state.proxy() as data:
            data['track_list'] = track_list
            data['track_id_list'] = choose_message_id
    
        await StateMachine.music_by_title_v2.set()


async def download_by_choice(call: types.CallbackQuery, state: FSMContext):
    
    answer = int(call.data)
    user_id = str(call.id) 
    state_data = await state.get_data()
    track_id_list = state_data['track_id_list']
    track_list_dict = state_data['track_list']
    track_list = tuple(track_list_dict)


    for message_id in track_id_list:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
        
            
    path = ROOT_DIR / user_id
    try:
        url = track_list[answer - 1]
        await call.message.answer('Downloading... it may take some time')
        await download(url=url, path=user_id)
        filename = track_list_dict[url]
        for name in os.listdir(path):
            if name.endswith('.mp3'):
                os.rename(f'{path}/{name}', f'{path}/{filename}.mp3')
                break
        file = f'{path}/{filename}.mp3'
        await bot.send_audio(call.message.chat.id, audio=open(file, 'rb'), title=f'{filename}.mp3')
    except Exception as ex:
        info(ex)
        await call.message.answer('Got unexpected issue, to start again -> enter /start', reply_markup=ReplyKeyboardRemove())
        return await state.finish()
    else:
        await call.message.answer('Do you want to do something else?', reply_markup=continuation_keyboard)
        return await state.finish()
    finally:
        if os.path.exists(path):
            await clear(path=path)


def handler_register(dp: Dispatcher):
    dp.register_message_handler(music_menu, Text(equals='Youtube Music'))
    dp.register_message_handler(search_by_title, Text(equals='Download by title'))
    dp.register_message_handler(get_music_by_title, state=StateMachine.music_by_title)
    dp.register_callback_query_handler(download_by_choice, state=StateMachine.music_by_title_v2)
    dp.register_message_handler(search_by_url, Text(equals='Download by URL'))
    dp.register_message_handler(download_by_url, state=StateMachine.music_by_url)