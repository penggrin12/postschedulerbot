from __future__ import annotations

import asyncio
import typing

from aiogram import Bot, Dispatcher
from aiogram_fsm_sqlitestorage import SQLiteStorage

from app.config import config

__all__: typing.List[str] = ["loop", "bot"]

loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(storage=SQLiteStorage("fsm.db"))
