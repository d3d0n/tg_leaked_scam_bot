from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ParseMode
import asyncio
from config import TOKEN2
import os




bot = Bot(token=TOKEN2)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет\nИспользуй /help')


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply('/dbtxt чтобы получить текстовый файл с картами\n/db чтобы получить .db файл\n/clear чтобы очистить файлы дб\n/txt чтобы получить данные из дб')

@dp.message_handler(commands=['dbtxt'])
async def process_dbtxt_command(message: types.Message):
    user_id = message.from_user.id
    file = open('cards.txt', 'rb')
    await message.reply_document(file)
    file.close()


@dp.message_handler(commands=['db'])
async def process_db_command(message: types.Message):
    user_id = message.from_user.id
    file = open('cards.db', 'rb')
    await message.reply_document(file)
    file.close()
    

@dp.message_handler(commands=['clear'])
async def process_db_command(message: types.Message):
    os.remove('cards.db')
    os.remove('cards.txt')
    await message.reply('готово')


@dp.message_handler(commands=['txt'])
async def process_help_command(message: types.Message):
    file = open('cards.txt', 'r')
    await message.reply(file.read())
    file.close()

if __name__ == '__main__':
    executor.start_polling(dp)
