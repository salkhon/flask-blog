from flask_wtf.form import FlaskForm
from wtforms.fields.simple import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField("Title", validators=[
        DataRequired()
    ])
    content = TextAreaField("Content", validators=[
        DataRequired()
    ])
    submit = SubmitField("Post")
