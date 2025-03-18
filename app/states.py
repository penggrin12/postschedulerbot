from aiogram.fsm.state import StatesGroup, State


class EnteringNewPost(StatesGroup):
    waiting = State()
