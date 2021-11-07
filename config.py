import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:admin@localhost:5433/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
