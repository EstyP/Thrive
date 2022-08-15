# **Thrive**
### Root for your plant, because it's your soil-mate!

**This web app helps you to identify the houseplants that you own, and explains how you can best care for them! You can register for your own account, where you can find the plants that you own and store them in your profile page, making it easy to find how to take care of them - such as how often you should water them, how much light they need, and how warm they need to be in order to Thrive!**

### Installation Guide

You will need to run the mysql scripts from the `schema.sql` file located in the `sql_scripts directory`. 

Update the information on `database.py` in line with your own database credentials

Copy the contents from `config.template.py` into a new python folder called `config.py`. Here, you will need to generate your own API id and key from https://www.back4app.com/database/back4app/list-of-largest-cities-in-uk and populate these into the corresponding fields

**You will need to install the following python packages:**
- **`pip install flask`**
- **`pip install mysql-connector-python`**
- **`pip install requests`**

Once you have followed these steps, run the program from your python IDE. Click the link that appears in the terminal, or navigate on your browser to `http://localhost:{port}`

This will display the login screen for the web app.

### Navigation

**Login Page**

Select the 'Sign Up' hyperlink which will redirect you to the sign up page. 

**Sign Up Page**

Enter your credentials here to register - username, email and password, and select your nearest UK city from the drop down selection. Once you have successfully registered, it will display a success message, and will redirect you to the login page. Type in your credentials and hit 'log in'.

**Home Page**

You will see a welcome message containing your name, and the local weather. From here, click 'Go to my profile', or on the top left corner, select the arrow next to the Thrive logo to display a drop down menu. Here, you can navigate to home, your profile, search plants, and log out. 

**Your Profile**

This will display your username and email address, and any plants you have added to your profile.

**Search Plants**

This will display images of all plants currently in the plants database.  Under each plant, you will see 'More info' and 'Add this plant' buttons. More info will open a 'modal' which will display all the information about how to care for this plant - ideal lighting conditions, maintenance level, watering frquency, soil conditions, humidity, temperature, and whether it's toxic or not. Click the C in the corner to close this and return to the search plants page. Clicking 'add this plant' will add the plant to your profile. Any plants currently in your profile will appear with 'remove this plant'. Clicking this will delete it from your profile. 

**Log Out**

Selecting log out returns you to the login screen. 

