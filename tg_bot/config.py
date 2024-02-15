from aiogram import Bot, Dispatcher, types
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


TOKEN = config("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()


async def set_commands():
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Баштоо"),
        types.BotCommand(command="list", description="кыска чыгармалардын тизмеси")
    ])