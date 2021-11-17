from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
