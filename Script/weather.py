from settings.config import TOKEN_WEATHER
import aiohttp
import datetime

async def get_weather(city,latitude, longitude):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    if city is None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={TOKEN_WEATHER}&units=metric") as response:
                    data = await response.json()
                    city = data["name"]
                    cur_weather = data["main"]["temp"]
                    humidity = data["main"]["humidity"]
                    pressure = data["main"]["pressure"]
                    wind = data["wind"]["speed"]
                    sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
                    sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
                    length_of_the_day = datetime.datetime.fromtimestamp(
                        data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                        data["sys"]["sunrise"])

                    weather_description = data["weather"][0]["main"]
                    if weather_description in code_to_smile:
                        wd = code_to_smile[weather_description]
                    else:
                        wd = "Посмотри в окно, не пойму что там за погода!"
                    res_weather_str = f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\nПогода в городе: {city}\nТемпература: {cur_weather}C° {wd}\nВлажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\nВосход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\nХорошего дня!"
                    return res_weather_str
        except Exception as ex:
            print(f"Error: {ex}")
            return('Error')
    else:
        try:
           async with aiohttp.ClientSession() as session:
               async with session.get(f"http://api.openweathermap.org/data/2.5/find?q={city}&appid={TOKEN_WEATHER}&units=metric") as response:
                    data = await response.json()
                    city = data["list"][0]['name']
                    cur_weather = data["list"][0]["main"]["temp"]
                    humidity = data["list"][0]["main"]["humidity"]
                    pressure = data["list"][0]["main"]["pressure"]
                    wind = data["list"][0]["wind"]["speed"]

                    weather_description = data["list"][0]["weather"][0]["main"]
                    if weather_description in code_to_smile:
                        wd = code_to_smile[weather_description]
                    else:
                        wd = "Посмотри в окно, не пойму что там за погода!"
                    res_weather_str = f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\nПогода в городе: {city}\nТемпература: {cur_weather}C° {wd}\nВлажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\nХорошего дня!"
                    return res_weather_str
        except Exception as ex:
            print(f'Error: {ex}')
            return('Error')

async def main_weather(city=None,latitude=55.45, longitude=65.3333):
    return await get_weather(city,latitude, longitude)
