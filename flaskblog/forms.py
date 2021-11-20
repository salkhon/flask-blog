from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # fileupload, file form validator
from wtforms.fields.simple import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from flaskblog.models import User

import flask_login
"""
Class based form creation that have built in validation methods.
"""


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(), Length(min=2, max=20)
    ])
    email = StringField("Email", validators=[
        DataRequired(), Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired()
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo("password")
    ])

    submit = SubmitField("Sign Up")

    # rather than validating uniqueness of the username before registration, we can use a custom validator.
    # validator format: validate_fieldtovalidate(). Automatically validates.
    def validate_username(self, username: StringField):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is already taken. Please choose another one.")

    def validate_email(self, email: StringField):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "That email is already taken. Please choose another one.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(), Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired()
    ])
    # We'll use cookies to remember user
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


# When we use these forms, we need to set a secret key for our application.
# Secret key will protect against modifying cookies, cross site requests, forgery attacks.

class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(), Length(min=2, max=20)
    ])
    email = StringField("Email", validators=[
        DataRequired(), Email()
    ])
    picture = FileField("Update Profile Picture", validators=[
        FileAllowed(["jpg", "png"])
    ])
    submit = SubmitField("Update")

    def validate_username(self, username: StringField):
        """
        Only checks if updated username conflicts with usernames that is not already the current uusername. 
        """
        if username.data != flask_login.current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "The username is taken. Please choose another username")

    def validate_email(self, email: StringField):
        """
        Only checks if updated email conflicts with emails that is not already the current uemail. 
        """
        if email.data != flask_login.current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "The email is taken. Please choose another email")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[
        DataRequired()
    ])
    content = TextAreaField("Content", validators=[
        DataRequired()
    ])
    submit = SubmitField("Post")
