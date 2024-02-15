from aiogram import Router, F, types
from aiogram.filters import Command
from tg_bot.key_boards.kb import get_stories


start_router = Router()

@start_router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(f"Привет! {message.from_user.full_name}")
    await message.answer(f"Кунуго бирден кыска чыгарма окуп турганга бул баскычты басыныз", reply_markup=get_stories())
