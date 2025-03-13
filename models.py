from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# User like table
post_likes = db.Table('post_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('timestamp', db.DateTime, default=datetime.utcnow)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    liked_posts = db.relationship('Post', secondary=post_likes, 
                                 backref=db.backref('liked_by', lazy='dynamic'))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def like_post(self, post):
        if not self.has_liked_post(post):
            self.liked_posts.append(post)
            return True
        return False
    
    def unlike_post(self, post):
        if self.has_liked_post(post):
            self.liked_posts.remove(post)
            return True
        return False
    
    def has_liked_post(self, post):
        return post in self.liked_posts
    
    def __repr__(self):
        return f'<User {self.email}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(150), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    @property
    def like_count(self):
        return self.liked_by.count()
    
    def __repr__(self):
        return f'<Post {self.id}>'