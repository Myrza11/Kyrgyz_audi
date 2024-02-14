from aiogram import Bot, Dispatcher, types
from decouple import config
from os import getenv
from db.base import DB

TOKEN = config("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher(bot)
db = DB()


async def set_commands():
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Начало"),
        types.BotCommand(command="pic", description="Получить картинку"),
        types.BotCommand(command="courses", description="Наши курсы"),
        types.BotCommand(command="free_lesson", description="Записаться на бесплатный урок"),
    ])