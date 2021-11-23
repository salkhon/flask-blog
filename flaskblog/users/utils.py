import os
import flask
import flask_mail
import secrets
import PIL.Image

import flaskblog
from flaskblog.models import User


def _save_picture(form_picture) -> str:
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename: str = random_hex + f_ext
    pic_path = os.path.join(flask.current_app.root_path,
                            "static/profile_pics", picture_filename)
    output_size = (125, 125)
    image: PIL.Image = PIL.Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(pic_path)
    return picture_filename


def _send_reset_email(user: User):
    token = user.get_reset_token()
    msg = flask_mail.Message(subject="Password Reset Request",
                             sender="noreply@demo.com", recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{flask.url_for("users.reset_token", token=token, _external=True)}

If you did not make this request then simply ignore this email and no change wil be made"""
    # _external=True is used to get absolute url rather than relative url.
    # complex email bodies can be rendered with jinja2 templates.
    flaskblog.mail.send(msg)
