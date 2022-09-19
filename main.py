from aiogram import executor, Dispatcher

from handlers import client, commands, other
from loader import dp
from utils.default import set_default_commands

async def on_startup(dp: Dispatcher):
    await set_default_commands(dp=dp)
    
    # handlers
    await commands.handler_register(dp=dp)
    await client.handler_register(dp=dp)
    await other.handler_register(dp=dp)


    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
