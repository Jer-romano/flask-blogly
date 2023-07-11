"""Blogly application."""
from flask import Flask, render_template, redirect, request
from sqlalchemy import text 
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'My secret key'

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def show_homepage():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('base.html', users=users)

@app.route('/users/new', methods=['GET'])
def show_user_form():
    return render_template('create_user.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    f_name = request.form['f_name']
    l_name = request.form['l_name']
    img = request.form['img_url']

    user = User(first_name = f_name, last_name=l_name, image_url=img)
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_page(user_id):
    user = User.query.get(user_id)
    return render_template('user_detail.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["GET"])
def show_edit_user_form(user_id):
    user = User.query.get(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    user = User.query.get(user_id)
    user.first_name = request.form['f_name']
    user.last_name = request.form['l_name']
    user.image_url = request.form['img_url']

    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')




