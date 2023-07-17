"""Blogly application."""
from flask import Flask, render_template, redirect, request
from sqlalchemy import text 
from models import db, connect_db, User, Post, Tag, PostTag
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
def show_users_and_tags():
    users = User.query.all()
    tags = Tag.query.all()
    return render_template('base.html', users=users, tags=tags)

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

@app.route('/users/<int:user_id>/posts/new')
def show_create_post_page(user_id):
    user = User.query.get(user_id) 
    tags = Tag.query.all()
    return render_template('create_post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    title = request.form['title']
    content = request.form['content']
    post = Post(title=title, content=content, author_id=user_id)
    db.session.add(post)
    db.session.commit()
    tags = request.form.getlist("tag_box")
    #need to get the ID of the post I just created
    new_post = Post.query.filter(Post.title == title, Post.content == content).one()
    for tag in tags:
        found_tag = Tag.query.filter_by(name=tag).first()
        pt = PostTag(post_id=new_post.id, 
        tag_id=found_tag.id)
        db.session.add(pt)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def show_edit_post_form(post_id):
    post = Post.query.get(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.author_id}')

@app.route("/tags/new")
def show_tag_form():
    return render_template('create_tag.html')

@app.route("/tags/new", methods=["POST"])
def process_tag_form():
    tag_name = request.form["tag"]
    tag = Tag(name=tag_name)
    db.session.add(tag)
    db.session.commit()
    return redirect("/users")

@app.route("/tags/<int:tag_id>")
def show_tag_detail(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template("tag_detail.html", tag=tag)

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/users')

@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def show_edit_tag_form(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    tag.name = request.form['tag']
    db.session.add(tag)
    db.session.commit()
    return redirect('/users')


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import update
# from your_module import YourModel

# # Create an engine and session
# engine = create_engine('your_database_url')
# Session = sessionmaker(bind=engine)
# session = Session()

# # Define the values you want to update
# new_value = "New Value"

# # Perform the update
# stmt = update(YourModel).where(YourModel.id == 1).values(attribute=new_value)
# session.execute(stmt)

# # Commit the transaction
# session.commit()