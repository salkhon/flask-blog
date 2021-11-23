import flaskblog  # init

if __name__ == "__main__":
    # Config values can be passed in with different email, pass, dbstring, key
    app = flaskblog.create_app()
    app.run(debug=True)
