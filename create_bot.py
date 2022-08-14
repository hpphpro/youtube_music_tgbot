from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML, disable_web_page_preview=False)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)