from aiogram import Router, F, types
from tg_bot.config import scheduler, bot
from tg_bot.db import queries



async def process_notify():
    scheduler.add_job(send_notification, "cron", hour=17, minute=55)
    scheduler.start()

async def send_notification():
    queries.init_db()
    story = queries.get_story()
    text = (f"{story[1]}\n\n"
            f"{story[2]}\n\n"
            )
    for user in queries.get_users():
        await bot.send_message(
            chat_id=user[2],
            text=text
        )

