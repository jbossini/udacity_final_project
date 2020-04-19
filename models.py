from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Comic
Information about the comics
'''


class Comic(db.Model):
    __tablename__ = 'Comics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    synopsis = db.Column(db.String())
    characters = db.Column(db.String(), nullable=False)
    series = db.Column(db.Integer, db.ForeignKey("Series.id"), nullable=False)

    def __init__(self, name, synopsis, characters, series):
        self.name = name
        self.synopsis = synopsis
        self.characters = characters
        self.series = series

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'synopsis': self.synopsis,
            'series': self.series}

    def __repr__(self):
        return json.dumps(self.format())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Series(db.Model):
    __tablename__ = 'Series'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    comics = db.relationship(
        'Comic', backref='series', lazy=True, cascade='delete')
    editorial = db.Column(db.Integer,db.ForeignKey("Editorial.id"),nullable=False)

    def __init__(self, name, comics, editorial):
        self.name = name
        self.comics = comics
        self.editorial = editorial

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'comics': self.comics,
            'editorial': self.editorial
        }

    def __repr__(self):
        return json.dumps(self.format())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Editorial(db.Model):
    __tablename__ = 'Editorial'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    address = db.Column(db.String())
    mail=db.Column(db.String(),nullable=False)
    series = db.relationship(
        'Series', backref='editorial', lazy=True, cascade='delete')
    
    def __init__(self, name, series, mail):
        self.name = name
        self.address = address
        self.series = series
        self.mail = mail

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'mail': self.mail,
            'series':self.series
        }

    def __repr__(self):
        return json.dumps(self.format())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()