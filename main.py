from aiogram import executor

from handlers import client, commands, other
from loader import dp

commands.handler_register(dp=dp)
client.handler_register(dp=dp)
other.handler_register(dp=dp)


    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
