from config import API_TOKEN, WEATHER_TOKEN
from utils import get_kb
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup
from datetime import date, datetime
import aiohttp
from zodiac_sign import get_zodiac_sign

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def greet_user(message: types.Message):
    await message.reply('Привет!', reply_markup=get_kb())


@dp.message_handler(regexp='^(Курс доллара)$')
async def get_currency(message: types.Message):
    async with aiohttp.ClientSession() as session:
        today = datetime.now().strftime('%d/%m/%Y')
        url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={today}&VAL_NM_RQ=R01235'
        async with session.get(url, ssl=False) as resp:
            data = await resp.text()
            try:
                soup = BeautifulSoup(data, 'xml')
                usd = soup.find('Valute', {'ID': 'R01235'}).find('Value').text
                await message.reply(usd, reply_markup=get_kb())
            except (KeyError, TypeError, ValueError):
                await message.reply('По выходным информации о курсе доллара нет :(', reply_markup=get_kb())



@dp.message_handler(regexp='^(Погода в Москве)$')
async def get_weather(message: types.Message):
    async with aiohttp.ClientSession() as session:
        city = 'Russia,Moscow'
        key = WEATHER_TOKEN
        url = f'http://api.worldweatheronline.com/premium/v1/weather.ashx?key={key}&q={city}&format=json&num_of_days=1'
        async with session.get(url, ssl=False) as resp:
            data = await resp.json()
            try:
                weather = data['data']['current_condition'][0]['temp_C']
                if '-' not in weather:
                    weather = '+' + weather
                await message.reply(f'В Москве сейчас {weather}°C', reply_markup=get_kb())
            except (KeyError, TypeError, ValueError):
                await message.reply('Сервис погоды временно недоступен', reply_markup=get_kb())


@dp.message_handler(regexp='^(Расскажи анекдот)$')
async def get_joke(message: types.Message):
    async with aiohttp.ClientSession() as session:
        url = 'https://www.anekdot.ru/random/anekdot/'
        async with session.get(url, ssl=False) as resp:
            data = await resp.text()
            soup = BeautifulSoup(data, 'html.parser')
            joke = soup.find('div', {'class': 'text'}).text
            await message.reply(joke, reply_markup=get_kb())


@dp.message_handler(regexp='^(Сколько осталось до Нового года)$')
async def new_year(message: types.Message):
    days = datetime(2023, 1, 1) - datetime.now()
    await message.reply(f'Дней: {days.days}, часов: {days.seconds // 3600}, минут: {(days.seconds // 60) % 60}', reply_markup=get_kb())


@dp.message_handler(regexp='^(Гороскоп на сегодня)$')
async def ask_date(message: types.Message):
    await message.reply('Введи дату рождения в формате ДД-ММ', reply_markup=get_kb())


@dp.message_handler()
async def get_prediction(message: types.Message):
    try:
        d = datetime.strptime(message.text, '%d-%m')
        date_of_birth = date(d.year, d.month, d.day)
        sign = get_zodiac_sign(date_of_birth)

        if (sign == "Aries"):
            sign = "Овен"
        elif (sign == "Taurus"):
            sign = "Телец"
        elif (sign == "Gemini"):
            sign = "Близнецы"
        elif (sign == "Cancer"):
            sign = "Рак"
        elif (sign == "Leo"):
            sign = "Лев"
        elif (sign == "Virgo"):
            sign = "Дева"
        elif (sign == "Libra"):
            sign = "Весы"
        elif (sign == "Scorpio"):
            sign = "Скорпион"
        elif (sign == "Sagittarius"):
            sign = "Стрелец"
        elif (sign == "Capricorn"):
            sign = "Козерог"
        elif (sign == "Aquarius"):
            sign = "Водолей"
        elif (sign == "Pisces"):
            sign = "Рыбы"

        async with aiohttp.ClientSession() as session:
            url = 'https://74.ru/horoscope/daily/'
            async with session.get(url, ssl=False) as resp:
                data = await resp.text()
                soup = BeautifulSoup(data, 'html.parser')
                predictions = soup.find_all('article', {'class': 'IGRa5'})
                prediction = filter(lambda p: p.find('h3').text == sign, predictions)
                prediction = list(prediction)[0].find_all('div')[-1].text
                await message.reply(prediction, reply_markup=get_kb())
    except ValueError:
        await message.reply('Введи дату рождения в формате ДД-ММ', reply_markup=get_kb())


if __name__ == '__main__':
    executor.start_polling(dp)
