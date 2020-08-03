from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize

from datetime import datetime

button_obnal = KeyboardButton(emojize(':credit_card: Обналичивание'))
button_check1 = KeyboardButton(emojize(':dollar: Чекер Баланса'))
button_check2 = KeyboardButton(emojize(':money_with_wings: Чекер на валидность'))

greet_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False
).add(button_obnal, button_check1, button_check2)


def checkmsg(number, date, cvv):
    chck = number.isnumeric() and cvv.isnumeric() and date[:2].isnumeric() and date[3:].isnumeric and date[2] == '/'
    if len(number) == 16 and len(date) == 5 and len(cvv) == 3:
        if int(number[0]) in [2, 3, 4, 5, 6] and int(date[3:]) > int(datetime.today().strftime('%y')) and chck:
            return True
        elif int(date[3:]) == int(datetime.today().strftime('%Y')[2:]):
            if int(date[:2]) < int(datetime.today().strftime('%m')):
                return True
            else:
                return False
        else:
            return False
    else:
        return False
