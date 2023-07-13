"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

def getCurrentDateTime():
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    return dt_string

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
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                        nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                            default=getCurrentDateTime())
    author_id = db.Column(db.Integer,
                          db.ForeignKey('users.id'))
    author = db.relationship('User', backref="posts")


 