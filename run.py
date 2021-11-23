import flaskblog  # init

if __name__ == "__main__":
    app = flaskblog.create_app()
    app.run(debug=True)
