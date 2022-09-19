from aiogram import Dispatcher, types

async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        commands=[
            types.BotCommand('start', 'Start bot'),
            types.BotCommand('stop', 'drop bot action'),
            types.BotCommand('cancel', 'drop bot action'),
        ]
    )
    