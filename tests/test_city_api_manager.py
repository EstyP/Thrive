import unittest
from city_api_manager import CityApiManager


class CityApiManagerTest(unittest.TestCase):

    def test_cities(self):
        city_api_manager = CityApiManager()
        self.assertIn('Aylesbury', city_api_manager.cities)
        self.assertNotIn('Lichfield', city_api_manager.cities)


if __name__ == '__main__':
    unittest.main()