from flask import Flask
from flaskblog.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # Flask password encryption
# We add some functionalities to our db models, and it will handle all the sessions in the background
from flask_login import LoginManager
import flask_mail
# we're going to need a mail server, mail port. TLS. username and password for that server.

# extensions not bound to flask instance, will be bound with passed in config when run.py is executed 
db = SQLAlchemy()

bcrypt = Bcrypt()

login_manager = LoginManager()
# redirects to login page if user_authentication is required but not done.
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

mail = flask_mail.Mail()


def create_app(config_cls=Config):
    app = Flask(__name__)
    app.config.from_object(config_cls)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.main.routes import main
    from flaskblog.posts.routes import posts
    from flaskblog.users.routes import users
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
