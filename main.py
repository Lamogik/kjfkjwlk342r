from aiogram.client.bot import DefaultBotProperties
from aiogram import Dispatcher
import asyncio
import logging

# импорты пакетов
from settings import settings
from handlers import user
from utils.commands import *
from middlewares.middlewares import *
from database.migration.db_migration import migration_db
from db_module import DataBase

db = DataBase()

# запуск процесса поллинга новых апдейтов
async def main(db):
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s - "
                                                   "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    # токен бота указать в файле input

    await migration_db(db)
    dp = Dispatcher()
    # подключает проверку подписки на канал
    dp.message.middleware()
    dp.message.middleware(AntiFlood())
    # роутеры
    dp.include_routers(
        user.router
    )

    # объект бота
    bot = Bot(token=settings.bots.bot_work_token)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main(db))
