from datetime import datetime
from flaskblog import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(
        db.String(20), nullable=False, default="default.jpg")  # going to be hashed
    password = db.Column(db.String(60), nullable=False)
    # one to many
    posts = db.relationship("Post", backref="author", lazy=True)
    # setting as instance variables in constructor don't work

    def __repr__(self):
        return f"User('{self.username}', {self.email}, '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # User model has the table name automatically set to user (lowercase)
    # can set own table name, set a table name attr.
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
