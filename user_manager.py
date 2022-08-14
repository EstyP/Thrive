from flask import session, redirect, url_for
from database import get_db_connection
import uuid


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


class UserManager:

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