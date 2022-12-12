from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton
)

from database.tools import CityTools


def generate_save_city_keyboard(city_name: str):
    markup = InlineKeyboardMarkup()  # Разметка
    markup.row(
        InlineKeyboardButton(text="Сохранить город", callback_data=f"save_{city_name}")
    )
    return markup


def generate_cities_keyboard(user_id: int):
    cities = CityTools().get_city_names(user_id)
    if cities:
        markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        markup.add(*cities)
        markup.row(
            KeyboardButton(text="✍ Редактировать список")
        )
    else:
        markup = ReplyKeyboardRemove()
    return markup


def generate_remove_cities_keyboard(user_id: int):
    markup = InlineKeyboardMarkup(row_width=2)
    cities = [
        InlineKeyboardButton(text=f"❌ {city}", callback_data=f"remove_{city}_{user_id}")
        for city in CityTools().get_city_names(user_id)
    ]
    markup.add(*cities)
    return markup
