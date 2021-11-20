import os
import flask
import secrets
from PIL import Image

import flaskblog
from flaskblog.models import User, Post
from flaskblog.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm
import flask_login


@flaskblog.app.route("/")
@flaskblog.app.route("/home")
def home():
    posts = Post.query.all()
    return flask.render_template("home.html", posts=posts)


@flaskblog.app.route("/about")
def about():
    return flask.render_template("about.html", title="About")


@flaskblog.app.route("/register", methods=["GET", "POST"])
def register():
    if flask_login.current_user.is_authenticated:
        flask.flash("You are already logged in!", "info")
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
        flask.flash(
            f"Your account has been created! You are now able to log in!", "success")

        return flask.redirect(flask.url_for("login"))

    return flask.render_template("register.html", title="Register", form=form)


@flaskblog.app.route("/login", methods=["GET", "POST"])
def login():
    if flask_login.current_user.is_authenticated:
        flask.flash("You are already logged in!", "info")
        return flask.redirect(flask.url_for("home"))

    form = LoginForm()

    if form.validate_on_submit():
        # rather than handling authentication on form validators - we use login_manager to maintain session.
        user = User.query.filter_by(email=form.email.data).first()
        if user and flaskblog.bcrypt.check_password_hash(user.password, form.password.data):
            flask_login.login_user(user, remember=form.remember.data)
            # can redirect to login from authentication screened pages. That way we have a next query param from the url.
            next_page = flask.request.args.get("next")
            return flask.redirect(next_page) if next_page else flask.redirect(flask.url_for("home"))
        else:
            flask.flash(
                "Login Unsuccessful. Please check email and password", "danger")

    return flask.render_template("login.html", title="Login", form=form)


@flaskblog.app.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for("home"))


def _save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    pic_path = os.path.join(flaskblog.app.root_path,
                            "static/profile_pics", picture_filename)
    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(pic_path)
    return picture_filename


@flaskblog.app.route("/account", methods=["GET", "POST"])
@flask_login.login_required
def account():
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
        return flask.redirect(flask.url_for("account"))
    elif flask.request.method == "GET":
        form.username.data = flask_login.current_user.username
        form.email.data = flask_login.current_user.email
    image_file = flask.url_for(
        "static", filename=f"profile_pics/{flask_login.current_user.image_file}")
    return flask.render_template("account.html", title="Account", image_file=image_file, form=form)


@flaskblog.app.route("/post/new", methods=["GET", "POST"])
@flask_login.login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        flask.flash("Your post has been created!", "success")
        post = Post(title=form.title.data, content=form.content.data,
                    author=flask_login.current_user)
        flaskblog.db.session.add(post)
        flaskblog.db.session.commit()
        return flask.redirect(flask.url_for("home"))
    return flask.render_template("create_post.html", title="New Post", form=form, legend="New Post")


@flaskblog.app.route("/post/<int:post_id>")  # variables of int type in route
def post(post_id):
    """GETs post of passed in post_id in the URL. Single page view of the required post. 

    Args:
        post_id (int): post_id of post to GET. int: in route restricts type of var. 
    """
    post = Post.query.get_or_404(
        post_id)  # if it does not exist return 404. If exists, render a template with that post
    return flask.render_template("post.html", title=post.title, post=post)


@flaskblog.app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@flask_login.login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != flask_login.current_user.id:
        flask.abort(403)  # Forbidden Route.
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        flaskblog.db.session.commit()
        flask.flash("Your post has been updated!", "success")
        return flask.redirect(flask.url_for("post", post_id=post.id))
    elif flask.request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    # we're going to make use of same tempate for create and update with params.
    # if this route was used to view create_post.html, form submit will POST on this route. 
    return flask.render_template("create_post.html", title="Update Post", form=form, legend="Update Post")


@flaskblog.app.route("/post/<int:post_id>/delete", methods=["POST"])
@flask_login.login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != flask_login.current_user.id:
        flask.abort(403)
    flaskblog.db.session.delete(post)
    flaskblog.db.session.commit()
    flask.flash("Your post has been deleted!", "success")
    return flask.redirect(flask.url_for("home"))
