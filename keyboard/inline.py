from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup 


__all__ = [
    'inline_button'
]

# creating a button when it invokes
def inline_button(text: str, callback: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text, callback_data=callback)
            ]
        ]
         
    )
