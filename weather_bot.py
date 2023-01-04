import requests

import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())


class FSMKblevels(StatesGroup):
    level_1 = State()
    level_2 = State()


async def on_startup(_):
    print('Все гуд')


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Добро пожаловать!\nЯ - <b>Погода-бот</b>, бот созданный чтобы всегда знать погоду."
                         "\n<b>Укажите город</b>", parse_mode='html')
    await FSMKblevels.level_1.set()

@dp.message_handler(content_types= 'text', state=FSMKblevels.level_1)
async def cites(message: types.Message):
        global city
        city = message.text
        keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Температура")
        item2 = types.KeyboardButton("Состояние погоды")
        item3 = types.KeyboardButton("Как мне одеться")
        item4 = types.KeyboardButton("Все сразу")
        item5 = types.KeyboardButton('Указать другой город')
        keybord.add(item1, item2, item3, item4, item5)

        await bot.send_message(message.from_user.id, 'Выберите, что хотите узнать', reply_markup=keybord)
        await FSMKblevels.level_2.set()


@dp.message_handler(state=FSMKblevels.level_2)
async def temp(message: types.Message):
    if message.text == 'Температура':

                r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru')
                data = r.json()
                name = data['name']
                cur_weather = round(data['main']['temp'])
        #description = weather.current.description
        #if description in code_description:
            #wd = code_description[description]
            #weather = await client.get(city)
                resp_msg =  name + "\n"
                resp_msg += f"Текущая температура: {cur_weather}°С"

                await bot.send_message(message.from_user.id, resp_msg)

    elif message.text == 'Состояние погоды':

                r = requests.get(
                    f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru')
                data = r.json()
                wd = data['weather'][0]['description']
                name = data['name']
            #weather = await client.get(city)
            #description = weather.current.description
            #if description in code_description:
                #wd = code_description[description]
                resp_msg = name + '\n'
                resp_msg += f'Текущие состояние погоды: {wd.capitalize()}'

                await bot.send_message(message.from_user.id, resp_msg)

    elif message.text == 'Как мне одеться':
            r = requests.get(
                f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru')
            data = r.json()
            name = data['name']
            cur_weather = round(data['main']['temp'])

            resp_msg = name + '\n'
            if cur_weather <= -30:
                    resp_msg += f'На улице {cur_weather}°C, одевайтесь как можно теплее!'
            elif -30 < cur_weather <= -10:
                    resp_msg += f'На улице {cur_weather}°C, одевайтесь очень тепло!'
            elif -10 < cur_weather <= 0:
                    resp_msg += f'На улице ниже 0, одевайтесь тепло, не забудьте про шапку'
            elif 0 < cur_weather < 18:
                    resp_msg += f'На улице прохладно, посоветовал бы надеть кофту'
            elif 18 <= cur_weather < 30:
                    resp_msg += f'На улице тепло, одевайтесь полегче'
            elif cur_weather >= 30:
                    resp_msg += f'На улице ужасно жарко: {cur_weather}°C,' \
                            f' советую остаться в доме лежать под кондиционером'

            await bot.send_message(message.from_user.id, resp_msg)

    elif message.text == 'Все сразу':
            r = requests.get(
                f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru')
            data = r.json()
            name = data['name']
            cur_weather = round(data['main']['temp'])
            wd = data['weather'][0]['description']
            #weather = await client.get(city)
            #description = weather.current.description
            #if description in code_description:
                #wd = code_description[description]
            resp_msg = name + '\n'
            resp_msg += f'Текущая температура: {cur_weather}°C\n'
            resp_msg += f'Текущее состояние погоды: {wd.capitalize()}\n\n'
            if cur_weather <= -30:
                    resp_msg += f'На улице {cur_weather}°C, одевайтесь как можно теплее!'
            elif -30 < cur_weather <= -10:
                    resp_msg += f'На улице {cur_weather}°C, одевайтесь очень тепло!'
            elif -10 < cur_weather <= 0:
                    resp_msg += f'На улице ниже 0, одевайтесь тепло, не забудьте про шапку'
            elif 0 < cur_weather < 18:
                    resp_msg += f'На улице прохладно, посоветовал бы надеть кофту'
            elif 18 <= cur_weather < 30:
                    resp_msg += f'На улице тепло, одевайтесь полегче'
            elif cur_weather >= 30:
                    resp_msg += f'На улице ужасно жарко: {cur_weather}°C,' \
                            f' советую остаться в доме лежать под кондиционером'

            await bot.send_message(message.from_user.id, resp_msg)
    elif message.text == 'Указать другой город':
        await bot.send_message(message.from_user.id, 'Укажите город:')
        await FSMKblevels.level_1.set()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)