import requests
from geopy.geocoders import Nominatim
from datetime import datetime


class WeatherInfo:
    def __init__(self, city_name: str):
        self.city_name = city_name
        self.URL = "https://api.openweathermap.org/data/2.5/weather"
        self.location = self.__get_location()
        self.PARAMS = {
            "lat": self.location.latitude,
            "lon": self.location.longitude,
            "appid": "e39ce5d12420e3b12bcb9ff17f256b24",
            "units": "metric",
            "lang": "ru"
        }

    def __get_location(self):
        """Получить имя города city_name, вернуть локацию location"""
        geolocator = Nominatim(user_agent="openweather")
        location_ = geolocator.geocode(self.city_name)
        return location_

    def __get_response(self):
        """Сделать GET запрос и вернуть ответ Response"""
        response = requests.get(self.URL, params=self.PARAMS)
        return response

    def get_weather(self) -> str:
        source = self.__get_response().json()
        weather_desc = source["weather"][0]["description"]
        weather_temp = source["main"]["temp"]
        weather_feels = source["main"]["feels_like"]
        weather_pressure = source["main"]["pressure"]
        weather_humidity = source["main"]["humidity"]
        weather_wind = source["wind"]["speed"]
        weather_clouds = source["clouds"]["all"]
        weather_sunrise = datetime.fromtimestamp(source["sys"]["sunrise"]).time()
        weather_sunset = datetime.fromtimestamp(source["sys"]["sunset"]).time()
        return f"Погода: {weather_desc}\n" \
               f"Темп: {weather_temp} 🌡\n" \
               f"Чувствуется как: {weather_feels}\n" \
               f"Давления: {weather_pressure}\n" \
               f"Влажность: {weather_humidity}\n" \
               f"Скорость ветра: {weather_wind}\n" \
               f"Облачность: {weather_clouds}\n" \
               f"Восход солнца: {weather_sunrise}\n" \
               f"Закат: {weather_sunset}\n"
