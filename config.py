import os


class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.getcwd(), "movies.db")}'
    JSON_AS_ASCII = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

