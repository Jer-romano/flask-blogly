from unittest import TestCase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text 
from models import User, db, Post, Tag, PostTag
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class PostTagModelTests(TestCase):


    @classmethod
    def setUpClass(cls):
        '''Class method that runs once before the suite of tests. This makes sure we have a user
        that we can link the posts to.'''
        user = User(first_name="John", last_name="Smith")
        post = Post(title="Example", content="This is a post")
        db.session.add_all([user, post])
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        '''Class method that deletes the user we made in setUp.'''
        users = User.query.all()
        posts = Post.query.all()
        for post,user in zip(posts, users):
            db.session.delete(post)
            db.session.delete(user)
        db.session.commit()

    def setUp(self):
        '''Clean up any existing tags'''
        entries = Tag.query.all()
        for entry in entries:
             db.session.delete(entry)
        db.session.commit()

    def tearDown(self):
        '''Clean up any fouled transaction, reset primary key value to 1'''
        db.session.rollback()
        db.session.execute(text('ALTER SEQUENCE tags_id_seq RESTART'))
    
    def test_create_tag(self):
        '''Tests creating a tag'''
        tag = {"tag": "frog-life"}
        with app.test_client() as client:
            resp = client.post("/tags/new", data=tag, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/tags/1"> frog-life </a></li>', html)
        
    def test_create_post_with_tag(self):
        tag = {"tag": "frog-life"}
        post = {"title": "The best day", "content": "Today was a good day",
         "tag_box": ["frog-life"]}
        with app.test_client() as client:
            client.post("/tags/new", data=tag)