import datetime

import bcrypt

# from app import app
import jwt
from flask import current_app

from server.db.database import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # def __init__(self, email, password):
    #     self.email = email
    #     self.password = bcrypt.hashpw(
    #         password,
    #         current_app.config.get('BCRYPT_LOG_ROUNDS')
    #     ).decode()

    # def encode_auth_token(self, user_id):
    #     """
    #     Generates the Auth Token
    #     :return: string
    #     """
    #     try:
    #         payload = {
    #             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
    #             'iat': datetime.datetime.utcnow(),
    #             'sub': user_id
    #         }
    #         return jwt.encode(
    #             payload,
    #             current_app.config.get('SECRET_KEY'),
    #             algorithm='HS256'
    #         )
    #     except Exception as e:
    #         return e
    #
    # @staticmethod
    # def decode_auth_token(auth_token):
    #     """
    #     Decodes the auth token
    #     :param auth_token:
    #     :return: integer|string
    #     """
    #     try:
    #         payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
    #         return payload['sub']
    #     except jwt.ExpiredSignatureError:
    #         return 'Signature expired. Please log in again.'
    #     except jwt.InvalidTokenError:
    #         return 'Invalid token. Please log in again.'


class Page(db.Model):
    __tablename__ = "page"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)


class Classification(db.Model):
    __tablename__ = "classification"

    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id), primary_key=True)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    description = db.Column(db.Text)

    page = db.relationship('Page', foreign_keys='Classification.page_id')


class Description(db.Model):
    __tablename__ = "description"

    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id), primary_key=True)
    description = db.Column(db.Text)

    page = db.relationship('Page', foreign_keys='Description.page_id')


class Visited(db.Model):
    __tablename__ = "visited"

    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id), primary_key=True)
    description = db.Column(db.Text)

    page = db.relationship('Page', foreign_keys='Visited.page_id')


class Token(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = Token.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False