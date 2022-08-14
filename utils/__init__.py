from aiogram.dispatcher.filters.state import State, StatesGroup

from dataclasses import dataclass
import time

class StateMachine(StatesGroup):
    music_by_url = State()
    music_by_title = State()
    music_by_titlev2 = State()
    

@dataclass
class Data:
    track_list: tuple | None = None


# block_list: dict = {}
# def spam_list(user_id):
#     global block_list

#     if block_list.get(user_id):
#         if (int(time.time()) - block_list[user_id]) >= 5:
#             del block_list[user_id]
        
#     return block_list

