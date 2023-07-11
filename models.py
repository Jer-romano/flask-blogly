"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

#Models go below

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(25),
                            nullable=False)
    last_name = db.Column(db.String(25),
                            nullable=False)
    image_url = db.Column(db.String(300))

    @classmethod
    def get_by_last_name(cls, last_name):
        '''Get all users with a particular last name'''
        return cls.query.filter_by(last_name=last_name).all()