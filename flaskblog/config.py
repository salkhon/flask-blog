import os


class Config:
    # config for CRSF keys, and Web Token generation for password reset
    # used for generating tokens (for password reset) (generated using secrets module)
    SECRET_KEY = "9f9ad0ecd4303f23b26b6da9cf549216"

    # config for SQLAlchemy
    # /// means relative from current file.
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"

    # config for flask_mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")
