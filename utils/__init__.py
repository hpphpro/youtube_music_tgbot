from aiogram.dispatcher.filters.state import State, StatesGroup

from dataclasses import dataclass
from functools import partial, wraps
from typing import Any, Awaitable, Callable, TypeVar, cast
import asyncio


T = TypeVar("T", bound=Callable[..., Any])


def sync_to_async(func: T):
    @wraps(func)
    async def run_in_executor(*args, **kwargs):
        loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, pfunc)

    return cast(Awaitable[T], run_in_executor)


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

