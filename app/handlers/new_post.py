from aiogram import F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message, User
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app import states
from app.bot import bot, dp
from app.config import config
from app.db.models import Post, post_lock


@dp.callback_query(F.data == "new-post")
async def handler_new_post(callback: CallbackQuery, state: FSMContext) -> None:
    assert isinstance(callback.message, Message)

    await state.set_state(states.EnteringNewPost.waiting)

    kbb = InlineKeyboardBuilder()
    kbb.row(
        InlineKeyboardButton(
            text="Cancel",
            callback_data="start",
        )
    )

    msg: Message | bool = await callback.message.edit_text(
        "Send the message you want to schedule...", reply_markup=kbb.as_markup()
    )
    assert isinstance(msg, Message)

    await state.update_data(msg_chat_id=msg.chat.id, msg_id=msg.message_id)


# @dp.message(states.EnteringNewPost.waiting)
@dp.message()
async def handler_waiting_for_post(message: Message, state: FSMContext) -> None:
    assert isinstance(message.from_user, User)

    await message.delete()

    content_id: str | None = (
        getattr(message, message.content_type)[-1].file_id
        if message.content_type == ContentType.PHOTO
        else (
            (
                getattr(message, message.content_type).file_id
                if hasattr(getattr(message, message.content_type), "file_id")
                else None
            )
            if message.content_type != ContentType.TEXT
            else None
        )
    )

    async with post_lock:
        await Post(
            {
                Post.chat_id: config.test_chat_id,
                Post.text: message.html_text if (message.text or message.caption) else None,
                Post.media_file_id: content_id,
                Post.media_type: message.content_type,
            }
        ).save()

    return  # TODO: for now

    data = await state.get_data()
    await state.clear()

    kbb = InlineKeyboardBuilder()
    kbb.row(
        InlineKeyboardButton(
            text="Back",
            callback_data="start",
        )
    )

    await bot.edit_message_text(
        chat_id=data["msg_chat_id"],
        message_id=data["msg_id"],
        text="Done.",
        reply_markup=kbb.as_markup(),
    )
