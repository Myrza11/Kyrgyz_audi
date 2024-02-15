from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from tg_bot.db.queries import insert_story, init_db


new_text_router = Router()


class FreeLessonReg(StatesGroup):
    name = State()
    desc = State()
    text = State()


@new_text_router.message(Command("new"))
async def start(message: types.Message, state: FSMContext):
    await state.set_state(FreeLessonReg.name)
    await message.answer("Введите название")


@new_text_router.message(Command("cancel"))
@new_text_router.message(F.text.lower() == "cancel")
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Текст кошулган жок")


@new_text_router.message(FreeLessonReg.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FreeLessonReg.desc)
    await message.answer("Текст ж/о кыскача маалымат жазыныз")


@new_text_router.message(FreeLessonReg.desc)
async def process_desc(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(FreeLessonReg.text)
    await message.answer("Текстти жазыныз")


@new_text_router.message(FreeLessonReg.text)
async def process_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    init_db()
    data = await state.get_data()
    insert_story(
        data['name'],
        data['description'],
        data['text'])
    await message.answer("Текст кошулду")
    await state.clear()

