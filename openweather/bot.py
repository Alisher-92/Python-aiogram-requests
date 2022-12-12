from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery

from keyboards import *
from openweather import WeatherInfo
from database.tools import UserTools, CityTools

# Бот - объект, который взаимодействует с пользователем
bot = Bot("5455102729:AAE4FJVFITPElv8KxaI5AACCp3R53LYd7l4")
# Dispatcher / Оператор - объект, который прослушивает действия пользователя
dp = Dispatcher(bot)


# Асинхронное программирования
# Короутины / Coroutine - асинхронные функции
@dp.message_handler(commands=["start"])
async def start(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    await register_user(message)
    await bot.send_message(chat_id, f"Добро пожаловать, {full_name} !")
    await request_city_name(message)


async def register_user(message: Message):
    UserTools().register_user(
        full_name=message.from_user.full_name,
        username=message.from_user.username,
        chat_id=message.chat.id
    )


async def request_city_name(message: Message):
    chat_id = message.chat.id
    user_id = UserTools().get_user_id(chat_id)
    await bot.send_message(chat_id, "Введите названия города: ",
                           reply_markup=generate_cities_keyboard(user_id))


@dp.message_handler(lambda message: message.text == "✍ Редактировать список")
async def edit_cities_list(message: Message, edit: bool = False):
    chat_id = message.chat.id
    message_id = message.message_id
    user_id = UserTools().get_user_id(chat_id)
    cities = CityTools().get_city_names(user_id)
    cities_message = "Ваш список городов:\n\n"
    i = 0
    for city in cities:
        i += 1
        cities_message += f"{i}. {city}\n"
    if edit:
        await bot.edit_message_text(cities_message, chat_id, message_id,
                                    reply_markup=generate_remove_cities_keyboard(user_id))
    else:
        await bot.send_message(chat_id, cities_message,
                               reply_markup=generate_remove_cities_keyboard(user_id))


@dp.message_handler(lambda message: not message.text.isdigit())
async def send_response(message: Message):
    """Принимает названия города. Отправляет погоду"""
    chat_id = message.chat.id
    city_name = message.text
    try:
        weather_info = WeatherInfo(city_name).get_weather()
    except AttributeError:
        await message.reply("Данный город не существует")
    else:
        await bot.send_message(chat_id, weather_info,
                               reply_markup=generate_save_city_keyboard(city_name))


@dp.callback_query_handler(lambda call: call.data.startswith("save"))
async def save_city(call: CallbackQuery):
    chat_id = call.message.chat.id
    city_name = call.data.split("_")[-1].capitalize()
    user_id = UserTools().get_user_id(chat_id)
    save_status = CityTools().save_city(user_id, city_name)
    if save_status:
        await bot.answer_callback_query(call.id, "Город успешно сохранён !")
        await request_city_name(call.message)
    else:
        await bot.answer_callback_query(call.id, "Этот город уже есть списке !")


@dp.callback_query_handler(lambda call: call.data.startswith("remove"))
async def remove_city(call: CallbackQuery):
    _, city_name, user_id = call.data.split("_")
    user_id = int(user_id)
    remove_status = CityTools().remove_city(user_id, city_name)
    if remove_status:
        await bot.answer_callback_query(call.id, f"Город: {city_name}. Успешно удалён !")
        await edit_cities_list(call.message, edit=True)
        await request_city_name(call.message)

executor.start_polling(dp, skip_updates=True)
