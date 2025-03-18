from __future__ import annotations
from asyncio import Lock
from enum import StrEnum, auto

from piccolo.columns import (
    Integer,
    BigSerial,
    Varchar,
)
from piccolo.table import Table


__all__: list[str] = [
    "user_lock",
    "post_lock",
    "User",
    "Post",
]
user_lock = Lock()
post_lock = Lock()


class User(Table):
    class Status(StrEnum):
        FREE = auto()
        PRO = auto()

    id = Integer(null=False, unique=True, primary_key=True)
    status = Varchar(null=False, default=Status.FREE, choices=Status)


class Post(Table):
    id = BigSerial(null=False, unique=True, primary_key=True)
    chat_id = Integer(null=False, default=None)

    text = Varchar(null=True, length=8192)  # x2 message limit cuz html markup
    media_file_id = Varchar(null=True, length=128)  # TODO: how big is it actually?
    media_type = Varchar(null=False, length=64)
