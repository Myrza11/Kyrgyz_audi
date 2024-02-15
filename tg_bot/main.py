import asyncio
import logging
from config import bot, dp, set_commands
from db import queries
from handlers import (
    process_notify,
    start_router,
    new_text_router
)


async def on_startup():
    await process_notify()
    queries.init_db()
    queries.create_tables()


async def main():
    await set_commands()
    dp.include_router(start_router)
    dp.include_router(new_text_router)

    dp.startup.register(on_startup)

    await dp.start_polling(bot)


if __name__ == "__main__":
    # включаем логи
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())