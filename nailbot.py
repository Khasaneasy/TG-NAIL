import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    level=logging.INFO
)
bot = Bot(token=TELEGRAM_TOKEN)

dp = Dispatcher()


# @dp.message(Command('price'))
# тут цена и услуги
# @dp.message(Command('contact'))
# сюда входит инст ватсап(и адрес работы и время)
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    """ Хендлер на команду start и ответ."""
    content = Text(
        "Доброго времени суток, ",
        Bold(message.from_user.full_name)
    )
    await message.answer(
        content
    )


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
