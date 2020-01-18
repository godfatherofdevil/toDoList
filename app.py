import os


if __name__ == "__main__":
    from todo import create_app

    app = create_app(os.getenv("TODO_ENV", "dev"))
    app.run(host="0.0.0.0", use_reloader=False)
