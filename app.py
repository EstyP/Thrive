from flask import Flask, render_template, request, redirect, url_for, session, make_response
from database import get_db_connection
from weather_manager import WeatherManager, CityManager
import re, uuid, hashlib, datetime, requests

app = Flask(__name__)

app.secret_key = 'thrive'
token = "5d492a658c111f"

city_manager = CityManager(token=token)
weather_manager = WeatherManager(city_name=city_manager.get_city().city)

@app.get('/')
def home():
    if loggedin():
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
                account = cursor.fetchone()
            return render_template("home.html", account=account, weather=weather_manager.get_weather(), city=city_manager.get_city())
    return redirect(url_for('login'))


@app.get('/login')
def get_login():
    if loggedin():
        return redirect(url_for('index'))
    # Generate random token that will prevent CSRF attacks
    token = uuid.uuid4()
    session['token'] = token
    return render_template('login.html', msg=None, token=token)


@app.post('/login')
def login():
    if loggedin():
        return redirect(url_for('home'))
    # Output message if there's an error
    msg = ''
    # Check if user submitted form
    if 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Retrieve hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        # Check if account exists within MYSQL DB
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
                account = cursor.fetchone()
                # Create session data
                if account:
                    session['loggedin'] = True
                    session['id'] = account['id']
                    session['username'] = account['username']
                    token = request.form['token']
                    msg = 'Logged in successfully !'
                    if 'rememberme' in request.form:
                        # Create hash to store as cookie
                        hash = account['username'] + request.form['password'] + app.secret_key
                        hash = hashlib.sha1(hash.encode())
                        hash = hash.hexdigest()
                        # The cookie expires in 90 days
                        expire_date = datetime.datetime.now() + datetime.timedelta(days=90)
                        resp = make_response('Success', 200)
                        resp.set_cookie('rememberme', hash, expires=expire_date)
                        # Update rememberme in accounts table to the cookie hash
                        cursor.execute('UPDATE users SET rememberme = %s WHERE id = %s', (hash, account['id']))
                        connection.commit()
                    return render_template('home.html', account=account, msg=msg, weather=weather_manager.get_weather(), city=city_manager.get_city())
                else:
                    # Account doesnt exist or username/password incorrect
                    msg = 'Incorrect username/password!'
        # Generate random token that will prevent CSRF attacks
    token = uuid.uuid4()
    session['token'] = token
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg, token=token)


# logout function, redirects to login page once complete
@app.get('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Remove cookie data
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('rememberme', expires=0)
    return resp


# registration function, checks for valid input in email and username field
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect to home page if logged-in
    if loggedin():
        return redirect(url_for('home'))
    # Output message if there's an error
    msg = ''
    # Check if user submitted form
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'city' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        city = request.form['city']
        # Hash password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        hashed_password = hash.hexdigest()
        # Check if account exists within MYSQL DB
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
                account = cursor.fetchone()
                # If account exists, show error message:
                if account:
                    msg = 'Account already exists !'
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid email address !'
                elif not re.match(r'[A-Za-z0-9]+', username):
                    msg = 'Name must contain only characters and numbers!'
                else:
                    cursor.execute('INSERT INTO users (id, username, password, email, city) VALUES (NULL, %s, %s, %s, %s)',
                                   (username, hashed_password, email, city))
                    connection.commit()
                    msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty
        msg = 'Please fill out the form!'
    return render_template('signup.html', msg=msg)



# users profile page
@app.route('/profile')
def profile():
    if loggedin():
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
                account = cursor.fetchone()
            return render_template("profile.html", account=account)
    return redirect(url_for('login'))


@app.get("/search_plants")
def search_plants():
    if loggedin():
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
                account = cursor.fetchone()
                cursor.execute('SELECT plant_name, common_name, url FROM plants')
                plant_data = cursor.fetchall()
            return render_template("search.html", account=account, plant_data=plant_data)
    return redirect(url_for('login'))

# @app.get("/search_plants", methods=['GET', 'POST'])
# def search_plants():
#     if loggedin():
#         if request.method == 'POST' and 'plant_name' in request.form:
#             plant_name = request.form['plant_name']
#             with get_db_connection() as connection:
#                 with connection.cursor(dictionary=True) as cursor:
#                     cursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
#                     account = cursor.fetchone()
#                     cursor.execute('SELECT plant_name, common_name, url FROM plants')
#                     plant_data = cursor.fetchall()
#                     if plant_data:
#                         msg = 'Plant is already in database'
#                     else:
#                         cursor.execute(
#                             'INSERT INTO user_plants (id, plant_name) VALUES (NULL, %s)',
#                             (session['id'], plant_name))
#                         connection.commit()
#                         msg = 'Plant successfully added!'
#
#         return render_template("search.html", account=account, plant_data=plant_data)
#     return redirect(url_for('login'))



def loggedin():
    if 'loggedin' in session:
        return True
    elif 'rememberme' in request.cookies:
        with get_db_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                # Check if user is remembered, cookie has to match the "rememberme"
                cursor.execute('SELECT * FROM users WHERE rememberme = %s', (request.cookies['rememberme'],))
                account = cursor.fetchone()
                if account:
                    # update session variables
                    session['loggedin'] = True
                    session['id'] = account['id']
                    session['username'] = account['username']
                    return True
    # If account isn't logged in, return false
    return False


if __name__ == "__main__":
    app.run(host="localhost", port=5003, debug=True)
