from sqlalchemy import null

from eapp.models import Post, User
from eapp import app, db
import hashlib

def authenticate(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password)).first()

def register_user(name, username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User(name=name, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_id(user_id):
    return User.query.get(user_id)

def upload_post(title, content, user_id):
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return True

def update_post(title, content, post_id):
    post = get_post_by_id(post_id)
    post.title = title
    post.content = content
    db.session.commit()

def delete_post(post_id):
    post = get_post_by_id(post_id)
    db.session.delete(post)
    db.session.commit()

def load_posts(kw=None, page=1):
    query = Post.query
    if kw:
        query = query.filter(Post.title.contains(kw))
    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    query = query.slice(start, start + page_size)

    return query.all()

def get_post_by_id(post_id):
    return Post.query.get_or_404(int(post_id))

def count_post():
    return Post.query.count()