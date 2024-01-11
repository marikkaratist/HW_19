from flask import Flask
from flask_restx import Api
from config import Config
from setup_db import db
from views.auth import auth_ns
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.user import user_ns


def create_app(config: Config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.app_context().push()
    configure_app(app)

    return app


def configure_app(app: Flask):
    db.init_app(app)
    db.create_all()
    api = Api(app)
    api.add_namespace(auth_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(user_ns)


app_ = create_app(Config())

if __name__ == '__main__':
    app_.run(host="localhost", port=10001, debug=True)
