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
    music_by_title_v2 = State()
