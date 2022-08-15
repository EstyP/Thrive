import unittest
import unittest.mock
from plant_manager import PlantManager

mock_plant_data = [
    {
        'plant_name': 'aglaonema',
        'common_name': 'chinese evergreen',
    },
    {
        'plant_name': 'alocasia',
        'common_name': 'elephant ear',
    }
]


def get_mock_db_cursor(fetchone_return_value=None, fetchall_return_value=None):
    return unittest.mock.Mock(
        __enter__=lambda _: unittest.mock.Mock(
            execute=lambda query, params: None,
            fetchone=lambda: fetchone_return_value,
            fetchall=lambda: fetchall_return_value,
        ),
        __exit__=lambda *args: None,
    )


def get_mock_db_connection(mock_db_cursor):
    return unittest.mock.Mock(
        __enter__=lambda _: unittest.mock.Mock(
            cursor=lambda **kwargs: mock_db_cursor,
        ),
        __exit__=lambda *args: None,
    )


class TestPlantManager(unittest.TestCase):

    def test_get_all_plant_data(self):
        plant_data = PlantManager.get_all_plant_data()
        # Assert that an example plant, the aglaonema, belongs to the plant data
        try:
            aglaonema = next(filter(lambda plant: plant['plant_name'] == 'aglaonema', plant_data))
        except StopIteration:
            self.fail('Example plant aglaonema is not in the database')
        else:
            self.assertEqual(aglaonema['common_name'], 'chinese evergreen')

    def test_get_plant_data_for_user(self):
        mock_user_id = 5
        mock_db_cursor = get_mock_db_cursor(fetchall_return_value=mock_plant_data)
        mock_db_connection = get_mock_db_connection(mock_db_cursor)
        with unittest.mock.patch('mysql.connector.connect', return_value=mock_db_connection):
            plant_data = PlantManager.get_plant_data_for_user(mock_user_id)
            self.assertSequenceEqual(plant_data, mock_plant_data)

    def test_get_plant_names_for_user(self):
        mock_user_id = 5
        mock_db_cursor = get_mock_db_cursor(fetchall_return_value=mock_plant_data)
        mock_db_connection = get_mock_db_connection(mock_db_cursor)
        with unittest.mock.patch('mysql.connector.connect', return_value=mock_db_connection):
            plant_names = PlantManager.get_plant_names_for_user(mock_user_id)
            self.assertSequenceEqual(plant_names, [plant['plant_name'] for plant in mock_plant_data])


if __name__ == '__main__':
    unittest.main()