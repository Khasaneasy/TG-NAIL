import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    """ Хендлер на команду start и ответ."""
    content = f"Доброго времени суток, <b>{message.from_user.full_name}</b>"
    await message.answer(content, parse_mode="HTML")


@dp.message(Command('price'))
async def cmd_price(message: types.Message):
    """ Хендлер на команду price."""
    prices = {
        'Маникюр': '1000 рублей',
        'Педикюр': '1500 рублей',
    }
    text = "Услуги и цены:\n\n"
    for service, price in prices.items():
        text += f'{service}: {price}\n'
    await message.answer(text, parse_mode="HTML")


@dp.message(Command('contact'))
async def cmd_contact(message: types.Message):
    """ Хендлер на команду contact и вывод контактной информации."""
    contact_info = {
        'Адрес': 'ул. Калмыкова, 20',
        'Время работы': '10:00 - 18:00',
        'Инстаграм': '@salon_beauty',
        'WhatsApp': '+799999999'
    }
    text = "Контактная информация:\n\n"
    for info_type, info in contact_info.items():
        text += f"{info_type}: {info}\n"
    await message.answer(text, parse_mode="HTML")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
