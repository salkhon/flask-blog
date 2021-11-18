import flask
from flask.helpers import flash

import flaskblog
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        "author": "Corey Schafer",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "April 20, 2018"
    },
    {
        "author": "Salman Khondker",
        "title": "Blog Post 2",
        "content": "Second post content",
        "date_posted": "April 21, 2018"
    }
]


@flaskblog.app.route("/")
@flaskblog.app.route("/home")
def home():
    return flask.render_template("home.html", posts=posts)


@flaskblog.app.route("/about")
def about():
    return flask.render_template("about.html", title="About")


@flaskblog.app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in!", "info")
        return flask.redirect(flask.url_for("home"))

    form = RegistrationForm()

    # after POST
    if form.validate_on_submit():
        hashed_pass = flaskblog.bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_pass)
        flaskblog.db.session.add(user)
        flaskblog.db.session.commit()

        # one time alert
        # "success" - bootstrap class
        flash(f"Your account has been created! You are now able to log in!", "success")

        return flask.redirect(flask.url_for("login"))

    return flask.render_template("register.html", title="Register", form=form)


@flaskblog.app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in!", "info")
        return flask.redirect(flask.url_for("home"))

    form = LoginForm()

    if form.validate_on_submit():
        # rather than handling authentication on form validators - we use login_manager to maintain session.
        user = User.query.filter_by(email=form.email.data).first()
        if user and flaskblog.bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # can redirect to login from authentication screened pages. That way we have a next query param from the url.
            next_page = flask.request.args.get("next")
            return flask.redirect(next_page) if next_page else flask.redirect(flask.url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")

    return flask.render_template("login.html", title="Login", form=form)


@flaskblog.app.route("/logout")
def logout():
    logout_user()
    return flask.redirect(flask.url_for("home"))


@flaskblog.app.route("/account")
@login_required
def account():
    return flask.render_template("account.html", title="Accout")
