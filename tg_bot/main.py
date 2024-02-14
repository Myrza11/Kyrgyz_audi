import asyncio
from aiogram import Bot
import logging
from config import bot, dp, db, set_commands
# from handlers import (
#     start_router,
#     picture_router,
#     echo_router,
#     courses_router,
#     free_lesson_reg_router
# )


async def on_startup(bot: Bot):
    db.create_tables()
    db.populate_tables()


async def main():
    await set_commands()
    # добавляем роутеры
    # dp.include_router(start_router)
    # dp.include_router(picture_router)
    # dp.include_router(courses_router)
    # dp.include_router(free_lesson_reg_router)

    # в самом конце
    # dp.include_router(echo_router)

    dp.startup.register(on_startup)
    # запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    # включаем логи
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())