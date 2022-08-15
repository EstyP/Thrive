from flask import Flask, session, request, flash, render_template, redirect, url_for
from config import flask_secret_key
from account_manager import AccountManager, should_be_logged_in, should_be_logged_out
from plant_manager import PlantManager
from city_api_manager import CityApiManager
from weather_api_manager import WeatherApiManager

app = Flask(__name__)
app.secret_key = flask_secret_key

user_manager = AccountManager()
plant_manager = PlantManager()
city_api_manager = CityApiManager()
weather_api_manager = WeatherApiManager()


@app.get('/login')
@should_be_logged_out
def view_login():
    token = AccountManager.create_csrf_token()
    return render_template('login.html', token=token)


@app.post('/login')
@should_be_logged_out
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    token = request.form.get('token')
    error_message = AccountManager.get_login_error_message(username, password, token)
    if error_message:
        flash(error_message)
        return redirect(url_for('view_login'))
    user_id = AccountManager.get_account_id(username)
    session['id'] = user_id
    return redirect(url_for('home'))


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
    error_message = AccountManager.get_signup_error_message(username, email, city, password)
    if error_message:
        flash(error_message)
        return redirect(url_for('view_signup'))
    AccountManager.add_account(username, email, city, password)
    flash('You have successfully registered! Please log in.')
    return redirect(url_for('view_login'))


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