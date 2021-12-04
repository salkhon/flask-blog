# type: ignore
from datetime import datetime

import flask
import flaskblog

from flask_login import UserMixin

from itsdangerous.jws import TimedJSONWebSignatureSerializer as Serializer

# Reloading the user from the user_id stored in the session.
# type: ignore

@flaskblog.login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

# The login manager extension expects the User model to have is_authenticated(), is_active(), is_anonymous(), get_id().
# Extension provides a class, from which we can inherit these common methods.

class User(flaskblog.db.Model, UserMixin):
    """
    Entity table. Can instantiate datarow with ctor. Queryies table, auto converts query return values to User obj. 
    User model has the table name automatically set to user (lowercase). Can set own table name, set a table name attr.
    """

    id = flaskblog.db.Column(flaskblog.db.Integer, primary_key=True)
    username = flaskblog.db.Column(
        flaskblog.db.String(20), unique=True, nullable=False)
    email = flaskblog.db.Column(
        flaskblog.db.String(120), unique=True, nullable=False)
    image_file = flaskblog.db.Column(
        flaskblog.db.String(20), nullable=False, default="default.jpg")  # going to be hashed
    password = flaskblog.db.Column(flaskblog.db.String(60), nullable=False)
    # one to many
    posts = flaskblog.db.relationship("Post", backref="author", lazy=True)
    # setting as instance variables in constructor don't work

    def get_reset_token(self, expires_sec=1800) -> str:
        """Uses itsdangerous TimedJSONWebSignatureSerializer to encode user_id payload to send it to unsecure 
        destinations. Generated token contains expiration. It allows us to handle expirations and tokens without
        needing to put all of that into a database and make things more complicated than they need to be.  

        Args:
            expires_sec (int, optional): expiry time in seconds. Defaults to 1800s (30 mins).

        Returns:
            string: userid serialized by itsdangerous serializer
        """
        s = Serializer(flask.current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({
            "user_id": self.id
        }).decode("utf-8")

    @staticmethod
    def verify_reset_token(token: str):
        """Decodes the token encoded by itsdangerous to get the payload.

        Args:
            token (string): object serialized using itdangerous. 

        Returns:
            obj: Decoded token. 
        """
        s = Serializer(flask.current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', {self.email}, '{self.image_file}')"


class Post(flaskblog.db.Model):
    """
    Entity table. Can instantiate datarow with ctor. Queryies table, auto converts query return values to post obj. 
    Post model has the table name automatically set to post (lowercase). Can set own table name, set a table name attr.
    """

    id = flaskblog.db.Column(flaskblog.db.Integer, primary_key=True)
    title = flaskblog.db.Column(flaskblog.db.String(100), nullable=False)
    date_posted = flaskblog.db.Column(
        flaskblog.db.DateTime, nullable=False, default=datetime.utcnow)
    content = flaskblog.db.Column(flaskblog.db.Text, nullable=False)

    user_id = flaskblog.db.Column(flaskblog.db.Integer, flaskblog.db.ForeignKey(
        "user.id"), nullable=False)
    # backref author

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
