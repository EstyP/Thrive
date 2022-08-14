import requests
from dataclasses import dataclass


@dataclass
class Weather:
    temperature: str
    wind: str
    description: str
    forecast: list


class WeatherApiManager:

    @staticmethod
    def get_weather(city) -> Weather:
        response = requests.get(f"https://goweather.herokuapp.com/weather/{city}")
        weather_data = response.json()
        return Weather(**weather_data)