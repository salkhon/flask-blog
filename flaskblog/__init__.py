import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # Flask password encryption
# We add some functionalities to our db models, and it will handle all the sessions in the background
from flask_login import LoginManager
import flask_mail
# we're going to need a mail server, mail port. TLS. username and password for that server.

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
# redirects to login page if user_authentication is required but not done.
login_manager.login_view = "login"
login_manager.login_message_category = "info"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS")
mail = flask_mail.Mail(app)
print("********************", os.environ.get("EMAIL_USER"))
