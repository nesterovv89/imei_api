import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from . import db, handlers

load_dotenv()

API_TOKEN = os.getenv('COMMON_TOKEN')
TELEGRAM_BOT_TOKEN = os.getenv('BOT_TOKEN')
API_URL = os.getenv('BACKEND_URL')

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()


async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    await db.create_tables()
    dp.include_routers(handlers.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
