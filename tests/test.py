from unittest import TestCase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text 
from models import User, db
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTests(TestCase):
    '''Tests for the User Model class'''
    def setUp(self):
        '''Clean up any existing users'''
        entries = User.query.all()
        for entry in entries:
            db.session.delete(entry)
        db.session.commit()

    def tearDown(self):
        '''Clean up any fouled transaction, reset primary key value to 1'''
        db.session.rollback()
        db.session.execute(text('ALTER SEQUENCE users_id_seq RESTART'))
    
    def test_list_users(self):
        '''Tests that all users in the db are listed on the page'''
        user1 = User(first_name="John", last_name="Smith", image_url="www.google.com")
        user2 = User(first_name="Jane", last_name="Goodall", image_url="www.chimps.com")
        user3 = User(first_name="Billy", last_name="Joel", image_url="www.piano.com")

        db.session.add_all([user1, user2, user3])
        db.session.commit()
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/users/1">John Smith</a></li>', html)
            self.assertIn('<li><a href="/users/2">Jane Goodall</a></li>', html)
            self.assertIn('<li><a href="/users/3">Billy Joel</a></li>', html)

    def test_add_new_user(self):
        '''Tests adding a new user to the page (and db)'''
        with app.test_client() as client:
            new_user = {"f_name": "John", "l_name": "Smith", "img_url": "www.google.com"}
            resp = client.post("/users/new", data=new_user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/users/1">John Smith</a></li>', html)
        
    def test_edit_user(self):
        '''Test for editing a user's info'''
        user1 = User(first_name="John", last_name="Smith", image_url="www.google.com")
        db.session.add(user1)
        db.session.commit()
        altered_user = {"f_name": "John", "l_name": "Wayne", "img_url": "www.google.com"}

        with app.test_client() as client:
            resp = client.post("/users/1/edit", data=altered_user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/users/1">John Wayne</a></li>', html)
    
    def test_delete_user(self):
        '''Test for deleting a user. Here we delete user1'''
        user1 = User(first_name="John", last_name="Smith", image_url="www.google.com")
        user2 = User(first_name="Jane", last_name="Goodall", image_url="www.chimps.com")
        user3 = User(first_name="Billy", last_name="Joel", image_url="www.piano.com")

        db.session.add_all([user1, user2, user3])
        db.session.commit()
        with app.test_client() as client:
            resp = client.post('/users/1/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('John Smith', html)
            self.assertIn('<li><a href="/users/2">Jane Goodall</a></li>', html)
            self.assertIn('<li><a href="/users/3">Billy Joel</a></li>', html)
    
    def test_get_by_last_name(self):
        '''Tests the class method for getting a user by their last name'''
        user1 = User(first_name="John", last_name="Smith", image_url="www.google.com")
        user2 = User(first_name="Jane", last_name="Goodall", image_url="www.chimps.com")
        user3 = User(first_name="Billy", last_name="Joel", image_url="www.piano.com")
        user4 = User(first_name="Wilfred", last_name="Goodall", image_url="www.youtube.com")

        db.session.add_all([user1, user2, user3, user4])
        db.session.commit()

        result = User.get_by_last_name('Goodall')
        self.assertEquals(result, [user2, user4])