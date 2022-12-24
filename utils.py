from aiogram.types import ReplyKeyboardMarkup


def get_kb():
    btns = [
        ['Курс доллара', 'Погода в Москве'],
        ['Расскажи анекдот'], ['Гороскоп на сегодня'],
        ['Сколько осталось до Нового года']
    ]
    return ReplyKeyboardMarkup(btns, resize_keyboard=True)
