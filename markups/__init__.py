from aiogram.types import ReplyKeyboardMarkup
from dataclasses import dataclass


@dataclass(frozen=True)
class Button:
    music_btn: str = 'Youtube Music'
    # other_btn: str = 'Another button'
    
    btn_search_title: str = 'Download by title'
    btn_search_url: str = 'Download by URL'

    choose_btns: tuple = ('1', '2', '3', '4', '5',)

    continuation_btns: tuple = ('Yes', 'No')

    back_to_menu: str = 'back'




# ----------------> main menu <----------------
menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*(Button.music_btn,))

# ----------------> Music menu <----------------
music_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
music_menu_keyboard.add(*(Button.btn_search_title, Button.btn_search_url,))
music_menu_keyboard.add(Button.back_to_menu)
music_choose_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*Button.choose_btns)

# ----------------> Afterline menu <----------------
continueation_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*Button.continuation_btns)