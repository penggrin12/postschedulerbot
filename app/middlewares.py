from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from app.db.models import User, user_lock


class EnsureDBUserMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not event.from_user:
            raise RuntimeError(f"No user on a message {event.message_id}@{event.chat.id}")

        async with user_lock:
            db_user: User = await User.objects().get_or_create(
                User.id == event.from_user.id,
                {
                    User.id: event.from_user.id,
                },
            )

        data["db_user"] = db_user

        return await handler(event, data)


class EnsureDBUserCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        async with user_lock:
            db_user: User = await User.objects().get_or_create(
                User.id == event.from_user.id,
                {
                    User.id: event.from_user.id,
                },
            )

        data["db_user"] = db_user

        return await handler(event, data)
