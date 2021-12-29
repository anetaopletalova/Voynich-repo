import json

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

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Classification(db.Model):
    __tablename__ = "classification"

    id = db.Column(db.Integer, unique=True, primary_key=True,
                   autoincrement=True)  # odpovida classification_id = na jedne strance jeden clovek co vse udelal
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id))
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(256))
    created_at = db.Column(db.String(128))
    markings = db.Column(db.JSON, default={})
    description = db.Column(db.Text)

    page = db.relationship('Page', foreign_keys='Classification.page_id')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    @property
    def serialized(self):
        return {
            'page_id': self.page_id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'created_at': self.created_at,
            'markings': json.loads(self.markings),
            'description': self.description
        }


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

    @property
    def serialized(self):
        return {
            'id': self.id,
            'classification_id': self.classification_id,
            'page_id': self.page_id,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'description': self.description,
        }


class Description(db.Model):
    __tablename__ = "description"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id))
    classification_id = db.Column(db.Integer, db.ForeignKey(Classification.id))
    description = db.Column(db.Text)

    page = db.relationship('Page', foreign_keys='Description.page_id')
    classification = db.relationship('Classification', foreign_keys='Description.classification_id')

    @property
    def serialized(self):
        return {
            'id': self.id,
            'page_id ': self.page_id,
            'classification_id': self.classification_id,
            'description': self.description,
        }


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

    classification = db.relationship('Classification', foreign_keys='Note.classification_id')
    user = db.relationship('User', foreign_keys='Note.user_id')


class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return '<id: token: {}'.format(self.token)


class Favorite(db.Model):
    __tablename__ = "favorite"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classification_id = db.Column(db.Integer, db.ForeignKey(Classification.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    classification = db.relationship('Classification', foreign_keys='Favorite.classification_id')
    user = db.relationship('User', foreign_keys='Favorite.user_id')

