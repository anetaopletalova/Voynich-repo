from datetime import datetime
from server.db.database import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Page(db.Model):
    __tablename__ = "page"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)


class Classification(db.Model):
    __tablename__ = "classification"

    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id))
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(256))
    created_at = db.Column(db.String(128))
    markings = db.Column(db.JSON, default={})
    description = db.Column(db.Text)

    page = db.relationship('Page', foreign_keys='Classification.page_id')


class Marking(db.Model):
    __tablename__ = "marking"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id))
    classification_id = db.Column(db.Integer, db.ForeignKey(Classification.id))
    description = db.Column(db.Text)

    page = db.relationship('Page', foreign_keys='Description.page_id')
    classification = db.relationship('Classification', foreign_keys='Description.classification_id')


class Visited(db.Model):
    __tablename__ = "visited"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classification_id = db.Column(db.Integer, db.ForeignKey(Classification.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    classification = db.relationship('Classification', foreign_keys='Visited.classification_id')
    user = db.relationship('User', foreign_keys='Visited.user_id')


class Note(db.Model):
    __tablename__ = "note"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    classification_id = db.Column(db.Integer, db.ForeignKey(Classification.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id))

    classification = db.relationship('Classification', foreign_keys='Note.classification_id')
    user = db.relationship('User', foreign_keys='Note.user_id')
    page = db.relationship('Page', foreign_keys='Note.page_id')


class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)


class Favorite(db.Model):
    __tablename__ = "favorite"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classification_id = db.Column(db.Integer, db.ForeignKey(Classification.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    classification = db.relationship('Classification', foreign_keys='Favorite.classification_id')
    user = db.relationship('User', foreign_keys='Favorite.user_id')
