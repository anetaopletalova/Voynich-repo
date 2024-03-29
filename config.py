import os
basedir = os.path.abspath(os.path.dirname(__file__))

# 'postgresql+psycopg2://postgres:admin@localhost:5432/Voynich'
# postgresql+psycopg2://postgres:postgres@localhost:12345/voynichdb
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://").replace('postgres://', 'postgresql://')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'RaGMe3V87xh6HLhb1+IWVKUnW5Byn1+Pf0jMMD7q7XwpCl2F/r4AhPpp95zMpFzqktrLd2ka5j' \
                 '+e4WyN3iXKTJKnUJ3k8qQDTG1wBQ30qPXf6y4xonY6tn' \
                 '/k8o5SXRnEDeI5A9dKzlPfD4cQ1u9YPihyLcDCKVcMHHdAG2vo4Icbqz4BihOG8LqiNc2mGuS7YnzADaNYfvZEnLA1GpqEH' \
                 '+Wxb4CjHMD9hL9RnkPb+DdaIxlxEGreoHQF+Lu9WBS7LH0m1qmUaZLPxn8R1H/k2mtjoAOK+BrqEO0lHI+GudA7LU3Gds' \
                 '/wc3wvVyFBMJjIZmjNP4kkKscGaA5Tfqdy2Q== '
    BCRYPT_LOG_ROUNDS = 13
    CLASSIFICATION_PATH = './data/voynich-manuscript-classifications.csv'

