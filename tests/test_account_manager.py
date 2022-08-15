import unittest
import unittest.mock
from account_manager import AccountManager


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

    def test_get_account(self):
        test_user_id = 1
        mock_user_account = {'id': test_user_id, 'username': 'A', 'email': 'B', 'city': 'C'}
        mock_db_cursor = get_mock_db_cursor(fetchone_return_value=mock_user_account)
        mock_db_connection = get_mock_db_connection(mock_db_cursor)
        with unittest.mock.patch('mysql.connector.connect', return_value=mock_db_connection):
            account = AccountManager.get_account(test_user_id)
            self.assertEqual(account, mock_user_account)

    def test_get_account_id(self):
        test_username = 'Nikita'
        mock_user_id = 2
        mock_db_cursor = get_mock_db_cursor(fetchone_return_value={'id': mock_user_id})
        mock_db_connection = get_mock_db_connection(mock_db_cursor)
        with unittest.mock.patch('mysql.connector.connect', return_value=mock_db_connection):
            account_id = AccountManager.get_account_id(test_username)
            self.assertEqual(account_id, mock_user_id)

    def test_encrypt_password(self):
        test_password = 'password1234'
        test_salt = 'taylorswift'
        hashed_password = AccountManager.encrypt_password(test_password, test_salt)
        self.assertEqual(hashed_password, '8df9714018b2218333001e18e5aa4247d4d44ad3')


if __name__ == '__main__':
    unittest.main()