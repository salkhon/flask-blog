from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # Flask password encryption
# We add some functionalities to our db models, and it will handle all the sessions in the background
from flask_login import LoginManager

app = Flask(__name__)
# ideally you want secret keys to be just some random characters.
# >>> import secrets
# >>> secrets.token_hex(16) # 16 bytes
# '9f9ad0ecd4303f23b26b6da9cf549216'
# ^ getting random chars in python.
# you'll want to make this environment variable
app.config["SECRET_KEY"] = "9f9ad0ecd4303f23b26b6da9cf549216"
# /// means relative from current file.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login" # redirects to login page if user_authentication is required but not done. 
login_manager.login_message_category = "info"
