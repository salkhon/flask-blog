import flask

errors = flask.Blueprint("error", __name__)


@errors.app_errorhandler(404)
def error_404(error):
    # returns error code, default 200 - so other routes did not need it
    return flask.render_template("errors/404.html"), 404


@errors.app_errorhandler(403)
def error_403(error):
    return flask.render_template("errors/403.html"), 403


@errors.app_errorhandler(500)
def error_500(error):
    return flask.render_template("errors/500.html"), 500

# there is another method called errorhandler instead of app_errorhandler - but that is for current Blueprint, not entire application
