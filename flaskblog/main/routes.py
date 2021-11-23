import flask

from flaskblog.models import Post

main = flask.Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home() -> str:
    page = flask.request.args.get("page", 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    # path params are used to identify specific resources, while query params are used to sort / filter those resoures
    return flask.render_template("home.html", posts=posts)


@main.route("/about")
def about() -> str:
    return flask.render_template("about.html", title="About")
