from flask import session, redirect, url_for
from database import get_db_connection
import re, uuid, hashlib


def should_be_logged_in(route_func):
    def decorated_route_func(*args, **kwargs):
        if not session.get('id'):
            return redirect(url_for('login'))
        return route_func(*args, **kwargs)
    decorated_route_func.__name__ = route_func.__name__
    return decorated_route_func


def should_be_logged_out(route_func):
    def decorated_route_func(*args, **kwargs):
        if session.get('id'):
            return redirect(url_for('home'))
        return route_func(*args, **kwargs)
    decorated_route_func.__name__ = route_func.__name__
    return decorated_route_func


class AccountManager:

    @staticmethod
    def get_account(user_id):
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT id, username, email, city FROM users WHERE id = %s', (user_id,))
                account = cursor.fetchone()
        return account

    @staticmethod
    def create_csrf_token():
        token = uuid.uuid4().hex
        session['token'] = token
        return token

    @staticmethod
    def get_account_id(username):
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
                account = cursor.fetchone()
        if account:
            return account['id']

    @staticmethod
    def get_login_error_message(username, password, token):
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT id, username, password, salt FROM users WHERE username = %s', (username,))
                account = cursor.fetchone()
        if not account:
            return 'Incorrect login details. Please try again.'
        else:
            hashed_password = AccountManager.encrypt_password(password, account['salt'])
            if hashed_password != account['password']:
                return 'Incorrect login details. Please try again.'
            elif token != session['token']:
                return 'There was an error. Please try again.'

    @staticmethod
    def get_signup_error_message(username, email, city, password):
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
                account_with_username = cursor.fetchone()
                cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
                account_with_email = cursor.fetchone()
        if not username:
            return 'Username cannot be empty.'
        elif not re.match(r'[A-Za-z0-9]+', username):
            return 'Name must contain only letters and numbers.'
        elif not password:
            return 'Password cannot be empty.'
        elif len(password) < 8:
            return 'Password cannot be less than 8 characters long.'
        elif not email:
            return 'Email cannot be empty.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return 'Email address is not valid.'
        elif not city:
            return 'City cannot be empty.'
        elif account_with_username is not None:
            return f'Username {username} is already taken.'
        elif account_with_email is not None:
            return f'Account with email {email} already exists.'

    @staticmethod
    def add_account(username, email, city, password):
        salt = uuid.uuid4().hex
        hashed_password = AccountManager.encrypt_password(password, salt)
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('INSERT INTO users (username, email, city, password, salt) VALUES (%s, %s, %s, %s, %s)',
                               (username, email, city, hashed_password, salt))
                connection.commit()

    @staticmethod
    def encrypt_password(password, salt):
        salted_password = password + salt
        hashed_password = hashlib.sha1(salted_password.encode()).hexdigest()
        return hashed_password