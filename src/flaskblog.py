from flask import Flask, render_template, url_for, redirect
from flask.helpers import flash
# url_for locates locations of files, instead of putting them in manually.
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# ideally you want secret keys to be just some random characters.
# >>> import secrets
# >>> secrets.token_hex(16) # 16 bytes
# '9f9ad0ecd4303f23b26b6da9cf549216'
# ^ getting random chars in python.

# you'll want to make this environment variable
app.config["SECRET_KEY"] = "9f9ad0ecd4303f23b26b6da9cf549216"

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


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    # after POST
    if form.validate_on_submit():
        # one time alert
        # "success" - bootstrap class
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)


if __name__ == "__main__":
    app.run(debug=True)
