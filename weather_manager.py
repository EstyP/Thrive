import requests
from requests import get
from dataclasses import dataclass

@dataclass
class Weather:
    temperature: str
    wind: str
    description: str
    forecast: list

@dataclass
class City:
    ip: str
    hostname: str
    city: str
    region: str
    country: str
    loc: str
    org: str
    postal: str
    timezone: str


class WeatherManager:
    def __init__(self, city_name: str):
        self.city_name = city_name
        self.weather = self._get_weather()

    def _get_weather(self) -> Weather:
        response = requests.get(f"https://goweather.herokuapp.com/weather/{self.city_name}")
        weather_data = response.json()
        return Weather(**weather_data)

    def get_weather(self) -> Weather:
        return self.weather


class CityManager:
    def __init__(self, token: str):
        self.token = token
        self.city = self._get_city()

    def _get_city(self) -> City:
        ip = get('https://api.ipify.org').text
        ip_response = requests.get(f"https://ipinfo.io/{ip}?token={self.token}")
        user_city = ip_response.json()
        return City(**user_city)

    def get_city(self) -> City:
        return self.city







