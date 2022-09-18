from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

__all__ = [
    'menu_keyboard',
    'music_menu_keyboard',
    'continuation_keyboard',
]
# ----------------> main menu <----------------
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Youtube Music')
        ]
    ],
    resize_keyboard=True, 
    
)

# ----------------> Music menu <----------------
music_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Download by title'),
            KeyboardButton(text='Download by URL'),
            
        ], 
        [
            KeyboardButton(text='back')
        ]
    ], 
    resize_keyboard=True, 
    
)

# ----------------> Afterline menu <----------------
continuation_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Yes'),
            KeyboardButton(text='No'),
        ]
    ],
    resize_keyboard=True, 
    
)