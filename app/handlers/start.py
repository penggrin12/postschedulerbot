from typing import Callable
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message, User
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot import dp


async def _shared_start(method: Callable, user_id: int) -> None:
    kbb = InlineKeyboardBuilder()
    kbb.row(
        InlineKeyboardButton(
            text="New Post",
            callback_data="new-post",
        )
    )

    await method("hiiii", reply_markup=kbb.as_markup())


@dp.message(CommandStart())
async def handler_start(message: Message, state: FSMContext) -> None:
    assert isinstance(message.from_user, User)

    await state.clear()
    await _shared_start(message.answer, message.from_user.id)


@dp.callback_query(F.data == "start")
async def handler_callback_start(callback: CallbackQuery, state: FSMContext) -> None:
    assert isinstance(callback.message, Message)

    await state.clear()
    await _shared_start(callback.message.edit_text, callback.from_user.id)
