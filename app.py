from flask import Flask, session, request, flash, render_template, redirect, url_for
from database import get_db_connection
from config import flask_secret_key
from user_manager import UserManager, should_be_logged_in, should_be_logged_out
from plant_manager import PlantManager
from city_api_manager import CityApiManager
from weather_api_manager import WeatherApiManager
import re, uuid, hashlib

app = Flask(__name__)
app.secret_key = flask_secret_key

user_manager = UserManager()
plant_manager = PlantManager()
city_api_manager = CityApiManager()
weather_api_manager = WeatherApiManager()


@app.get('/login')
@should_be_logged_out
def view_login():
    token = UserManager.create_csrf_token()
    return render_template('login.html', token=token)


@app.post('/login')
@should_be_logged_out
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    token = request.form.get('token')
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute('SELECT id, username, password, salt FROM users WHERE username = %s', (username,))
            account = cursor.fetchone()
            if not account:
                flash('Incorrect login details. Please try again.')
            else:
                salt = account['salt']
                salted_password = password + salt
                hashed_password = hashlib.sha1(salted_password.encode()).hexdigest()
                if hashed_password != account['password']:
                    flash('Incorrect login details. Please try again.')
                elif token != session['token']:
                    flash('There was an error. Please try again.')
                else:
                    session['id'] = account['id']
                    return redirect(url_for('home'))
    return redirect(url_for('view_login'))


@app.get('/logout')
@should_be_logged_in
def logout():
    session.pop('id')
    return redirect(url_for('login'))


@app.get('/signup')
@should_be_logged_out
def view_signup():
    return render_template('signup.html', cities=city_api_manager.cities)


@app.post('/signup')
@should_be_logged_out
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    city = request.form.get('city')
    password = request.form.get('password')
    with get_db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            account_with_username = cursor.fetchone()
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            account_with_email = cursor.fetchone()
            if not username:
                flash('Username cannot be empty.')
            elif not re.match(r'[A-Za-z0-9]+', username):
                flash('Name must contain only letters and numbers.')
            elif not password:
                flash('Password cannot be empty.')
            elif len(password) < 8:
                flash('Password cannot be less than 8 characters long.')
            elif not email:
                flash('Email cannot be empty.')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Email address is not valid.')
            elif not city:
                flash('City cannot be empty.')
            elif account_with_username is not None:
                flash(f'Username {username} is already taken.')
            elif account_with_email is not None:
                flash(f'Account with email {email} already exists.')
            else:
                # Hash password
                salt = uuid.uuid4().hex
                salted_password = password + salt
                hashed_password = hashlib.sha1(salted_password.encode()).hexdigest()
                cursor.execute('INSERT INTO users (username, email, city, password, salt) VALUES (%s, %s, %s, %s, %s)',
                               (username, email, city, hashed_password, salt))
                connection.commit()
                flash('You have successfully registered! Please log in.')
                return redirect(url_for('view_login'))
    return redirect(url_for('view_signup'))


@app.get('/')
@should_be_logged_in
def home():
    account = user_manager.get_account(session['id'])
    return render_template('home.html', account=account, weather=weather_api_manager.get_weather(account['city']))


@app.route('/profile')
@should_be_logged_in
def profile():
    account = user_manager.get_account(session['id'])
    user_plants = plant_manager.get_plant_data_for_user(session['id'])
    return render_template('profile.html', account=account, user_plants=user_plants)


@app.get("/search_plants")
@should_be_logged_in
def search_plants():
    account = user_manager.get_account(session['id'])
    plant_data = plant_manager.get_all_plant_data()
    user_plants = plant_manager.get_plant_names_for_user(session['id'])
    return render_template('search.html', account=account, user_plants=user_plants, plant_data=plant_data)


@app.post("/add_plant/<plant_name>")
@should_be_logged_in
def add_plant(plant_name):
    plant_manager.add_plant_for_user(plant_name, session['id'])
    return redirect(url_for('search_plants'))


@app.post("/remove_plant/<plant_name>")
@should_be_logged_in
def remove_plant(plant_name):
    plant_manager.remove_plant_for_user(plant_name, session['id'])
    return redirect(url_for('search_plants'))


if __name__ == "__main__":
    app.run(host="localhost", port=5003, debug=True)