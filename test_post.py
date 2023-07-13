from unittest import TestCase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text 
from models import User, db, Post
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class PostModelTests(TestCase):
    '''Tests for the Post Model class'''

    @classmethod
    def setUpClass(cls):
        '''Class method that runs once before the suite of tests. This makes sure we have a user
        that we can link the posts to.'''
        user = User(first_name="John", last_name="Smith")
        db.session.add(user)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        '''Class method that deletes the user we made in setUp.'''
        entries = User.query.all()
        for entry in entries:
            db.session.delete(entry)
        db.session.commit()

    def setUp(self):
        '''Clean up any existing posts'''
        entries = Post.query.all()
        for entry in entries:
            db.session.delete(entry)
        db.session.commit()

    def tearDown(self):
        '''Clean up any fouled transaction, reset primary key value to 1'''
        db.session.rollback()
        db.session.execute(text('ALTER SEQUENCE posts_id_seq RESTART'))
    
    def test_create_post(self):
        '''Tests creating a post'''
        post = {"title": "My first post", "content":"Here is some interesting content"}
        with app.test_client() as client:
            resp = client.post("/users/1/posts/new", data=post, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/posts/1">My first post </a></li>', html)
    
    def test_view_post(self):
        '''Tests viewing the details of a post'''
        post = {"title": "My first post", "content":"Here is some interesting content"}
        with app.test_client() as client:
            client.post("/users/1/posts/new", data=post, follow_redirects=True)
            resp = client.get("/posts/1")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("My first post", html)
            self.assertIn("Here is some interesting content", html)
            self.assertIn("By John Smith", html)

    def test_edit_post(self):
        '''Tests editing a post'''
        post = {"title": "My first post", "content":"Here is some interesting content"}
        edited_post = {"title": "My edited post", "content":"Here is some edited content"}
        with app.test_client() as client:
            client.post("/users/1/posts/new", data=post, follow_redirects=True)
            resp = client.post("/posts/1/edit", data=edited_post, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("My edited post", html)
            self.assertIn("Here is some edited content", html)
            self.assertIn("By John Smith", html)
    
    def test_delete_post(self):
        '''Tests deleting a post'''
        post = {"title": "My first post", "content":"Here is some interesting content"}
        with app.test_client() as client:
            client.post("/users/1/posts/new", data=post, follow_redirects=True)
            resp = client.post("/posts/1/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("No posts yet!", html)
            self.assertNotIn("My first post", html)

