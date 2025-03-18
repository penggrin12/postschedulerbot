from aiogram import F
from aiogram.types import CallbackQuery

from app.bot import dp


@dp.callback_query(F.data == "ihavenoting")
async def handler_emptybutton(callback: CallbackQuery) -> None:
    await callback.answer()
