import json
import requests
import config


class CityApiManager:

    def __init__(self):
        self.__cities = self.initialise_cities()

    @staticmethod
    def initialise_cities():
        criteria = json.dumps({
            "population": {
                "$gt": 50000
            }
        })
        url = f"https://parseapi.back4app.com/classes/City?limit=500&order=name&keys=name&where={criteria}"
        headers = {
            'X-Parse-Application-Id': config.city_api_app_id,

            'X-Parse-Master-Key': config.city_api_key,
        }
        return [city['name'] for city in requests.get(url, headers=headers).json()['results']]

    @property
    def cities(self):
        return self.__cities