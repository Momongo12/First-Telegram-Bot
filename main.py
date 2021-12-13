import json
import os
import shutil
from pathlib import Path
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram.types.message import ContentType
import time
from Script.weather import main_weather
from Script.corona import get_data_corona
from Script.scrapper_news import all_news, top_five_news
from settings.keyboards import kb_news, kb_markup, kb_weather
from settings.config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher(bot)
time = time.localtime(time.time())


@dp.message_handler(commands=['start'])
async def callback_start(message: Message):
    path = Path("data", "HiSticker.tgs")
    with open(path, 'rb') as sticker:
        await bot.send_sticker(message.chat.id, sticker)
        await bot.send_message(chat_id=message.chat.id, text="Привет\U0001F600\nМеня зовут Лупа\nЯ твой бот помощник\U0001F916\nФункции которые я могу выполнять ты можешь увидеть ниже\U0001F447", reply_markup=kb_markup)


@dp.message_handler(lambda message: message.text)
async def callback(message: Message):
    if message.text == 'Новости':
        await bot.send_message(chat_id=message.chat.id, text="Какие новости вы бы хотели посмотреть:",
                               reply_markup=kb_news)
    elif message.text == "Погода":
        await message.answer(text='Выберите удобный для вас способ получения погоды', reply_markup=kb_weather)
    elif message.text == "Ввести город":
        await message.answer(text="Введите город на англ.\nНапример: город: Kurgan")
    elif 'ГОРОД:' in message.text.upper():
        await message.reply(text="Город успешно получен\U0001F44C\nДелаю запрос погоды...")
        ans = await main_weather(city=message.text[7:])
        if ans == 'Error':
            await message.answer(text="Проверьте город", reply_markup=kb_weather)
        else:
            await message.answer(text=ans)
    elif message.text == "\U00002B05 Назад":
        await message.answer(text="\U00002B05", reply_markup=kb_markup)
    elif message.text == "Коронавирус":
        await send_stat_corona(message)
    else:
        print(message.text)


async def send_stat_corona(message):
    total_in_region = await get_data_corona()
    corona_str = f"""***Статистика по коронавирусу на {time.tm_year}-{time.tm_mon}-{time.tm_mday}-{time.tm_hour}-{time.tm_min}-{time.tm_sec}***\n
Всего в Курганском регионе:\n{total_in_region['all_cases']} заболеваний\n{total_in_region['died']} смертей\n{total_in_region['cured']} вылечились\n
За сутки:\n{total_in_region['all_cases_today']} заболевших\n{total_in_region['died_today']} умерших\n{total_in_region['cured_today']} выздоровевших\n
Надевайте маску \U0001F637
Берегите себя \U0001F609
***Хорошего дня \U0001F600***"""
    await bot.send_message(message.chat.id, corona_str)


@dp.message_handler(content_types=ContentType.LOCATION)
async def send_weather(message: Message):
    longitude = message.location.longitude
    latitude = message.location.latitude
    print("Локация успешно получена\nДелаю запрос погоды...")
    ans = await main_weather(latitude=latitude, longitude=longitude)
    await bot.send_message(chat_id=message.chat.id, text=ans)

async def delete_folders():
    """Deleting folders with pictures for previous days month"""
    for day in range(1, time.tm_mday):
        path = Path("data", f'date_img_from_{time.tm_mday}_{day}')
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except Exception as ex:
                print(f"Error remove folder - {ex}")

@dp.callback_query_handler(lambda mes: mes.data == 'all_news')
async def callback_message(message: Message):
    res = await all_news()
    if res is None:
        await bot.send_message(message.from_user.id, f"Видимо новостей за сегодня еще нет\U0001F610\nЗайдите попозже:)")
    else:
        with open(Path('data','data_news.json'), encoding="utf-8") as file:
            card_news = json.load(file)
            for i in card_news:
                path = Path('data', f'date_img_from_{time.tm_mon}_{time.tm_mday}',f"{i['code_img']}" )
                with open(path, "rb") as photo:
                    await bot.send_photo(
                        message.from_user.id,
                        photo,
                        caption=i["title"] + '\n' + i["sub_title"] + '\n' + "Источник: " + i['sourсe'],
                        disable_notification=True
                    )
        await delete_folders()

@dp.callback_query_handler(lambda mes: mes.data == 'top_five')
async def callback_message(message: Message):
    res = await top_five_news()
    if res is None:
        await bot.send_message(message.from_user.id, f"Видимо новостей за сегодня еще нет\U0001F610\nЗайдите попозже:)")
    else:
        for i in res:
            path = Path('data', f'date_img_from_{time.tm_mon}_{time.tm_mday}', f"{i['code_img']}")
            with open(path, "rb") as photo:
                await bot.send_photo(
                    message.from_user.id,
                    photo,
                    caption=i["title"] + '\n' + i["sub_title"] + '\n' + "Источник: " + i['sourсe'],
                    disable_notification=True
                )

if __name__ == "__main__":
    executor.start_polling(dp)
