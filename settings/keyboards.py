from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Location
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='Погода'),
                                                          KeyboardButton(text="Коронавирус"),
                                                          KeyboardButton(text='Новости'))

kb_news = InlineKeyboardMarkup().row(InlineKeyboardButton(text="Все новости за сегодня", callback_data="all_news"),
                                     InlineKeyboardButton(text="Лучшие новости", callback_data="top_five"))

kb_weather = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text='Отправить геолокацию', request_location=True)).add(
    KeyboardButton(text="Ввести город")
).add(KeyboardButton(text='\U00002B05 Назад'))
