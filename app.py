from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_mysqldb import MySQL
import MySQLdb.cursors, re, uuid, hashlib, datetime, os

app = Flask(__name__)

app.secret_key = 'your secret key'  # to be amended, will be used to keep client side secure

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'thrive'

mysql = MySQL(app)

csrf_protection = False


# Login function
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect to home page if logged-in
    if loggedin():
        return redirect(url_for('index'))
    # Output message if there's an error
    msg = ''
    # Check if user submitted form
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Retrieve hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest();
        # Check if account exists within MYSQL DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password,))
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
                hash = hash.hexdigest();
                # The cookie expires in 90 days
                expire_date = datetime.datetime.now() + datetime.timedelta(days=90)
                resp = make_response('Success', 200)
                resp.set_cookie('rememberme', hash, expires=expire_date)
                # Update rememberme in accounts table to the cookie hash
                cursor.execute('UPDATE user SET rememberme = %s WHERE id = %s', (hash, account['id'],))
                mysql.connection.commit()
                return render_template('index.html', msg=msg)
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
        # Generate random token that will prevent CSRF attacks
    token = uuid.uuid4()
    session['token'] = token
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg, token=token)


# logout function, redirects to login page once complete
@app.route('/logout')
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
        return redirect(url_for('index'))
    # Output message if there's an error
    msg = ''
    # Check if user submitted form
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Hash password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        hashed_password = hash.hexdigest();
        # Check if account exists within MYSQL DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists, show error message:
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Name must contain only characters and numbers!'
        else:
            cursor.execute('INSERT INTO user (id, username, password, email) VALUES (NULL, %s, %s, %s)',
                           (username, hashed_password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)


# homepage will display once successfully logged in
@app.route('/index')
def index():
    if loggedin():
        return render_template("index.html", username=session['username'])
    return redirect(url_for('login'))


# users profile page
@app.route('/display')
def display():
    if loggedin():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE id = % s', (session['id'],))
        account = cursor.fetchone()
        return render_template("display.html", account=account)
    return redirect(url_for('login'))


# update details page
@app.route('/update', methods=['GET', 'POST'])
def update():
    msg = ''
    if loggedin():
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE username = % s', (username,))
            account = cursor.fetchone()
            # if account:
            #     msg = 'Account already exists !'
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute(
                    'UPDATE user SET  username =% s, password =% s, email =% s WHERE id =% s',
                    (username, password, email,
                     (session['id'],),))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg=msg)
    return redirect(url_for('login'))


# search page
@app.route('/search', methods=['GET', 'POST'])
def search():
    if loggedin():
        if request.method == "POST":
            plant = request.form['plant']
            cursor = mysql.connection.cursor()
            # search by plant name
            cursor.execute("SELECT plant_name, common_name from plants WHERE plant_name LIKE %s OR common_name LIKE %s",
                           ([plant], [plant]))
            mysql.connection.commit()
            data = cursor.fetchall()
            # all in the search box will return all the tuples
            if len(data) == 0 and plant == 'all':
                cursor.execute("SELECT plant_name, common_name from plants")
                mysql.connection.commit()
                data = cursor.fetchall()
            return render_template('search.html', data=data)
        return render_template('search.html')


# page to add new plants to the database
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    msg = ''
    if loggedin():
        if request.method == 'POST' and 'plant_name' in request.form and 'common_name' in request.form and 'light' in request.form and 'maintenance' in request.form and 'water_days' in request.form and 'soil_water_indicator' in request.form and 'toxic' in request.form and 'humidity' in request.form and 'environment_temp' in request.form:
            plant_name = request.form['plant_name']
            common_name = request.form['common_name']
            light = request.form['light']
            maintenance = request.form['maintenance']
            water_days = request.form['water_days']
            soil_water_indicator = request.form['soil_water_indicator']
            toxic = request.form['toxic']
            humidity = request.form['humidity']
            environment_temp = request.form['environment_temp']
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM plants WHERE plant_name = % s', (plant_name,))
            plant = cursor.fetchone()
            if plant:
                msg = 'Plant already in database'
            else:
                cursor.execute(
                    'INSERT INTO plants (plant_id, plant_name, common_name, light, maintenance, water_days, soil_water_indicator, toxic, humidity, environment_temp) VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s)',
                    (plant_name, common_name, light, maintenance, water_days, soil_water_indicator, toxic, humidity,
                     environment_temp), )
                mysql.connection.commit()
                msg = 'Plant successfully added !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template('insert.html', msg=msg)
    return redirect(url_for('login'))

#page to add new plants to the database
@app.route('/user_plants', methods=['GET', 'POST'])
def user_plants():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'plant_name' in request.form:
            plant_name = request.form['plant_name']
            cursor = mysql.connection.cursor()
            cursor.execute('select id from user where id = % s', (session['id'],))
            id = cursor.fetchall()
            id = [i[0] for i in id]  # [(id,)] -> [id]
            query = 'insert into user_plants (id, plant_name) values(%s, %s)'
            values = (id[0], plant_name)
            cursor.execute(query, values)
            mysql.connection.commit()
            msg = 'Plant successfully added !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template('user_plants.html', msg=msg)
    return redirect(url_for('login'))

@app.route("/view_plants", methods=['GET'])
def view_plants():
    if loggedin():
        if request.method == "GET":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT plant_name FROM plants')
            data = cursor.fetchall()
        return render_template("view_plants.html", data=data)
    return redirect(url_for('login'))

def loggedin():
    if 'loggedin' in session:
        return True
    elif 'rememberme' in request.cookies:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Check if user is remembered, cookie has to match the "rememberme"
        cursor.execute('SELECT * FROM user WHERE rememberme = %s', (request.cookies['rememberme'],))
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
    app.run(host="localhost", port=int("5003"))


