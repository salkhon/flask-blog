from typing import Union
import flask
import flask_login
from werkzeug.wrappers.response import Response
import flaskblog
from flaskblog.models import Post, User

from flaskblog.users.forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm
from flaskblog.users.utils import _save_picture, _send_reset_email

users = flask.Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register() -> Union[str, Response]:
    if flask_login.current_user.is_authenticated:  # type: ignore
        flask.flash("You are already logged in!", "info")
        return flask.redirect(flask.url_for("main.home"))

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
        flask.flash(
            f"Your account has been created! You are now able to log in!", "success")

        return flask.redirect(flask.url_for("users.login"))

    return flask.render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login() -> Union[str, Response]:
    if flask_login.current_user.is_authenticated:  # type: ignore
        flask.flash("You are already logged in!", "info")
        return flask.redirect(flask.url_for("main.home"))
    form = LoginForm()

    if form.validate_on_submit():
        # rather than handling authentication on form validators - we use login_manager to maintain session.
        user = User.query.filter_by(email=form.email.data).first()
        if user and flaskblog.bcrypt.check_password_hash(user.password, form.password.data):
            flask_login.login_user(user, remember=form.remember.data)
            # can redirect to login from authentication screened pages. That way we have a next query param from the url.
            next_page = flask.request.args.get("next")
            return flask.redirect(next_page) if next_page else flask.redirect(flask.url_for("main.home"))
        else:
            flask.flash(
                "Login Unsuccessful. Please check email and password", "danger")

    return flask.render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout() -> Response:
    flask_login.logout_user()
    return flask.redirect(flask.url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@flask_login.login_required
def account() -> Union[str, Response]:
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            pic_filename = _save_picture(form.picture.data)
            flask_login.current_user.image_file = pic_filename

        flask_login.current_user.username = form.username.data
        flask_login.current_user.email = form.email.data
        flaskblog.db.session.commit()
        flask.flash("Your account has been updated!", "success")
        # redirect for post-get-redirect pattern.
        # runs GET instead of POST, to avoid resubmit notification when page is reloaded
        return flask.redirect(flask.url_for("users.account"))
    elif flask.request.method == "GET":
        form.username.data = flask_login.current_user.username  # type: ignore
        form.email.data = flask_login.current_user.email  # type: ignore
    image_file: str = flask.url_for(
        "static", filename=f"profile_pics/{flask_login.current_user.image_file}")  # type: ignore

    return flask.render_template("account.html", title="Account", image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username: str) -> str:
    page = flask.request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return flask.render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request() -> Union[str, Response]:
    if flask_login.current_user.is_authenticated:  # type: ignore
        flask.flash("You are already logged in!", "info")
        return flask.redirect(flask.url_for("main.home"))

    form = RequestResetForm()

    if form.validate_on_submit():
        user: User = User.query.filter_by(email=form.email.data).first()
        # send the user an email with the token with which they can reset their password
        _send_reset_email(user)
        flask.flash(
            "An email has been sent with instructions to reset your password", "info")
        return flask.redirect(flask.url_for("users.login"))

    return flask.render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<string:token>", methods=["GET", "POST"])
def reset_token(token) -> Union[str, Response]:
    """User resets the password. To make sure that the user is the account holder, we need to make sure that the token
    we gave them in the email is active. We wil get that token from the URL. By sending them an email with a text
    containing this token, we will know that it's them when they navigate to this route. 
    """
    if flask_login.current_user.is_authenticated:  # type: ignore
        flask.flash("You are already logged in", "info")
        return flask.redirect(flask.url_for("main.home"))

    user = User.verify_reset_token(token)
    if not user:
        flask.flash("That is an invalid or expired token", "warning")
        return flask.redirect(flask.url_for("users.reset_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = flaskblog.bcrypt.generate_password_hash(
            form.password.data)
        user.password = hashed_password  # update
        flaskblog.db.session.commit()
        flask.flash("Your password has been updated!", "success")
        return flask.redirect(flask.url_for("main.home"))

    return flask.render_template("reset_token.html", title="Reset Password", form=form)
