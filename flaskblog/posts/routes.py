from typing import Union
import flask
import flask_login
from werkzeug.wrappers.response import Response
import flaskblog
from flaskblog.models import Post

from flaskblog.posts.forms import PostForm

posts = flask.Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@flask_login.login_required
def new_post() -> Union[str, Response]:
    form = PostForm()

    if form.validate_on_submit():
        flask.flash("Your post has been created!", "success")
        post = Post(title=form.title.data, content=form.content.data,
                    author=flask_login.current_user)
        flaskblog.db.session.add(post)
        flaskblog.db.session.commit()
        return flask.redirect(flask.url_for("main.home"))

    return flask.render_template("create_post.html", title="New Post", form=form, legend="New Post")


@posts.route("/post/<int:post_id>")  # variables of int type in route
def post(post_id) -> str:
    """GETs post of passed in post_id in the URL. Single page view of the required post. 

    Args:
        post_id (int): post_id of post to GET. int: in route restricts type of var. 
    """
    post = Post.query.get_or_404(
        post_id)  # if it does not exist return 404. If exists, render a template with that post
    return flask.render_template("post.html", title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@flask_login.login_required
def update_post(post_id) -> Union[str, Response]:
    post = Post.query.get_or_404(post_id)
    if post.author.id != flask_login.current_user.id:
        flask.abort(403)  # Forbidden Route.

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        flaskblog.db.session.commit()
        flask.flash("Your post has been updated!", "success")
        return flask.redirect(flask.url_for("posts.post", post_id=post.id))
    elif flask.request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    # we're going to make use of same tempate for create and update with params.
    # if this route was used to view create_post.html, form submit will POST on this route.
    return flask.render_template("create_post.html", title="Update Post", form=form, legend="Update Post")


@posts.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
@flask_login.login_required
def delete_post(post_id) -> Response:
    post = Post.query.get_or_404(post_id)

    if post.author.id != flask_login.current_user.id:
        flask.abort(403)

    flaskblog.db.session.delete(post)
    flaskblog.db.session.commit()
    flask.flash("Your post has been deleted!", "success")
    return flask.redirect(flask.url_for("main.home"))
