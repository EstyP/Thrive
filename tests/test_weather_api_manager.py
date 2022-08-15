import unittest
import unittest.mock
from weather_api_manager import WeatherApiManager


class WeatherApiManagerTest(unittest.TestCase):

    def test_get_weather_with_mock_values(self):
        mock_temperature = 'A'
        mock_wind = 'B'
        mock_description = 'C'
        mock_forecast = ['D']
        mock_weather = unittest.mock.Mock(
            status_code=200,
            json=lambda: {
                'temperature': mock_temperature,
                'wind': mock_wind,
                'description': mock_description,
                'forecast': mock_forecast,
            }
        )
        with unittest.mock.patch('requests.get', return_value=mock_weather):
            weather = WeatherApiManager.get_weather('London')
            self.assertEqual(weather.temperature, mock_temperature)
            self.assertEqual(weather.wind, mock_wind)
            self.assertEqual(weather.description, mock_description)
            self.assertSequenceEqual(weather.forecast, mock_forecast)


if __name__ == '__main__':
    unittest.main()