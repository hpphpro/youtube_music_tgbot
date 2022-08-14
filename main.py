from aiogram import executor

from handlers import client, commands, handler_register
from create_bot import dp

commands.handler_register(dp=dp)
handler_register(dp=dp)
client.handler_register(dp=dp)



    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
