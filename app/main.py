from __future__ import annotations
from typing import List

from aiogram.enums import ContentType
from piccolo.table import Table, TableMetaclass
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app import db, handlers  # noqa: F401
from app.bot import bot, dp, loop
from app.db import models
from app.logger import logger
from app.logger import setup as setup_logger
from app.middlewares import (
    EnsureDBUserMessageMiddleware,
    EnsureDBUserCallbackMiddleware,
)


async def create_db_tables() -> None:
    table: Table
    for table in [getattr(models, x) for x in models.__all__]:
        if not issubclass(type(table), (Table, TableMetaclass)):
            continue
        await table.create_table(if_not_exists=True)


async def run_bot() -> None:
    dp.message.outer_middleware(EnsureDBUserMessageMiddleware())
    dp.callback_query.outer_middleware(EnsureDBUserCallbackMiddleware())

    await dp.start_polling(bot)


async def run_scheduler() -> None:
    scheduler = AsyncIOScheduler()

    async def _job() -> None:
        posts: List[models.Post] = [
            models.Post(post, True)  # type: ignore
            for post in (
                await models.Post.select().order_by(models.Post.id).group_by(models.Post.chat_id)
            )
        ]

        for post in posts:
            await models.Post.delete().where(models.Post.id == post.id)

            match post.media_type:
                case ContentType.TEXT:
                    await bot.send_message(
                        chat_id=post.chat_id,
                        text=post.text,
                        parse_mode="HTML",
                    )
                case ContentType.PHOTO:
                    await bot.send_photo(
                        chat_id=post.chat_id,
                        caption=post.text,
                        photo=post.media_file_id,
                        parse_mode="HTML",
                    )
                case ContentType.VIDEO:
                    await bot.send_video(
                        chat_id=post.chat_id,
                        caption=post.text,
                        video=post.media_file_id,
                        parse_mode="HTML",
                    )
                case ContentType.VIDEO_NOTE:
                    await bot.send_video_note(
                        chat_id=post.chat_id,
                        video_note=post.media_file_id,
                    )
                case ContentType.ANIMATION:
                    await bot.send_animation(
                        chat_id=post.chat_id,
                        caption=post.text,
                        animation=post.media_file_id,
                        parse_mode="HTML",
                    )
                case ContentType.AUDIO:
                    await bot.send_audio(
                        chat_id=post.chat_id,
                        caption=post.text,
                        audio=post.media_file_id,
                        parse_mode="HTML",
                    )
                case ContentType.STICKER:
                    await bot.send_sticker(
                        chat_id=post.chat_id,
                        sticker=post.media_file_id,
                    )
                case _:
                    await bot.send_document(
                        chat_id=post.chat_id,
                        caption=post.text,
                        document=post.media_file_id,
                        parse_mode="HTML",
                    )

    scheduler._eventloop = loop
    scheduler.start()
    scheduler.add_job(_job, "cron", minute=0, second=0)


def main() -> None:
    setup_logger()

    try:
        loop.run_until_complete(create_db_tables())

        loop.create_task(run_scheduler())
        loop.create_task(run_bot())

        loop.run_forever()

    except KeyboardInterrupt:
        logger.info("Bot stopped")
