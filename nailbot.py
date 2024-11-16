import asyncio
import datetime
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
INSTAGRAM_URL = "https://www.instagram.com/bogatyreva_nailss"
WHATSAPP_URL = "https://wa.me/79897440671"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


engine = create_engine('sqlite:///databse.sqlite')
Base = declarative_base()


class Nail(Base):
    __tablename__ = 'nail'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    date = Column(DateTime)
    time = Column(DateTime)
    service = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


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

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Цены', callback_data='prices')],
    ])

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@dp.message(Command('contact'))
async def cmd_contact(message: types.Message):
    """ Хендлер на команду contact и вывод контактной информации."""
    contact_info = {
        'Адрес': 'https://2gis.ru/nalchik/geo/70030076168477659',
        'Время работы': '10:00 - 18:00'
    }
    text = "Контактная информация:\n\n"
    for info_type, info in contact_info.items():
        text += f"{info_type}: {info}\n"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Instagram",
            url=INSTAGRAM_URL,
            callback_data='contact_info')],
        [InlineKeyboardButton(
            text="WhatsApp",
            url=WHATSAPP_URL)]
    ])

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@dp.callback_query(lambda call: call.data == 'prices')
async def process_price_callback(callback_query: types.CallbackQuery):
    """Обработчик для кнопки 'Цены'."""
    await callback_query.answer("Цены на услуги", show_alert=True)


@dp.callback_query(lambda call: call.data == 'contact_info')
async def process_contact_callback(callback_query: types.CallbackQuery):
    """Обработчик для кнопки 'Контакты'."""
    await callback_query.answer("Контактная информация", show_alert=True)


@dp.message(content_types=types.TEXT)
async def cmd_appoitment(message: types.Message):
    """Хэндлер на запись и проверка доступности"""
    try:
        datetime_str = message.text
        datetime_obj = datetime.datetime.strptime(datetime_str, '%d.%m.%Y %H:%M')
    except ValueError:
        await message.answer(
            'Неверный формат даты и времени. Пожалуйста, используйте формат ДД.ММ.ГГГГ ЧЧ:ММ.')
        return

    date_time = datetime_obj.strptime('%d.%m.%Y %H:%M')
    service = 'Маникюр'
    existing_appointment = session.query(Nail).filter_by(
        date=date_time,
        service=service).first()

    if existing_appointment:
        await message.answer(
            'К сожалению, в это время уже есть запись. Пожалуйста, выберите другое время.')
    else:
        new_appoitment = Nail(user_id=message.from_user.id,
                              date=date_time,
                              service=service)
        session.add(new_appoitment)
        session.commit()
        await message.answer('Вы успешно записаны на " + date_time + ".')

        reminder_time = datetime_obj - datetime.timedelta(hours=1)
        job = bot.create_job(send_reminder,
                             when=reminder_time,
                             chat_id=message.chat.id,
                             text=f"Напоминание: у вас записан маникюр на завтра ({date_time}) в салоне красоты.")
        await job.schedule()


def send_reminder(chat_id: int, text: str):
    """ Функция для отправки напоминания."""
    return bot.send_message(chat_id, text)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
