from aiogram import Router, F, types
from aiogram.filters import Command
from tg_bot.db.queries import insert_user, init_db, get_random_books, get_story_by_id

call_router = Router()

@call_router.callback_query(F.data.startswith("get_books"))
async def get_stories(callback: types.CallbackQuery):
    init_db()
    insert_user(callback.from_user.full_name, callback.from_user.id)
    await callback.message.answer('Эми сиз кунуго бирден кыска чыгарма окуп турасыз🥳')


@call_router.callback_query(F.data.startswith("read_"))
async def get_stories(callback: types.CallbackQuery):
    init_db()
    id = callback.data.replace("read_")
    book = get_story_by_id(int(id))
    await callback.message.answer("")

