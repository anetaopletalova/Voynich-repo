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


class Page(db.Model):
    __tablename__ = "page"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Classification(db.Model):
    __tablename__ = "classification"

    id = db.Column(db.Integer, unique=True, primary_key=True) #odpovida classification_id = na jedne strance jeden clovek co vse udelal
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id))

    page = db.relationship('Page', foreign_keys='Classification.page_id')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Marking(db.Model):
    __tablename__ = "marking"

    id = db.Column(db.Integer, primary_key=True)
    classification_id = db.Column(db.Integer, db.ForeignKey(Classification.id))
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id))
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    description = db.Column(db.Text)

    page = db.relationship('Page', foreign_keys='Marking.page_id')
    classification = db.relationship('Classification', foreign_keys='Marking.classification_id')


class Description(db.Model):
    __tablename__ = "description"

    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id))
    classification_id = db.Column(db.Integer, db.ForeignKey(Classification.id))
    description = db.Column(db.Text)

    page = db.relationship('Page', foreign_keys='Description.page_id')
    classification = db.relationship('Classification', foreign_keys='Description.classification_id')


class Visited(db.Model):
    __tablename__ = "visited"

    id = db.Column(db.Integer, primary_key=True)
    # mozna nebude potreba ani page_id
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id), primary_key=True)
    classification_id = db.Column(db.Integer, db.ForeignKey(Classification.id), primary_key=True)

    classification = db.relationship('Classification', foreign_keys='Visited.classification_id')
    page = db.relationship('Page', foreign_keys='Visited.page_id')



class Token(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
