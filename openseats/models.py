from openseats import db
from werkzeug.utils import secure_filename
import os 
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    userID = db.Column(db.String(50), unique=True, nullable=False)
    userMessage = db.Column(db.String(200), unique=False, nullable=True)
    groups = db.relationship('Group', backref='owner')
    # join_requests = db.relationship('JoinRequest', backref='user', lazy='dynamic')
    def __repr__(self):
      return f"<User('{self.id}', '{self.username}', '{self.email}')>"


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    images = db.relationship('Image', backref='group_set', lazy=True)
    # join_requests = db.relationship('JoinRequest', backref='group', lazy='dynamic')

class JoinRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_title = db.Column(db.String(255), nullable=False)
    message_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('User', backref='join_request')
    group = db.relationship('Group', backref='join_request')

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    user = db.relationship('User', backref='reservation')
    group = db.relationship('Group', backref='reservation')

class Community_post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    content = db.Column(db.Text, nullable=False)
    # likes = db.relationship('Community_like', lazy='subquery', backref=db.backref('liked_posts', lazy=True))
    # dislikes = db.relationship('Community_dislike', lazy='subquery',backref=db.backref('disliked_posts', lazy=True))
    
    user = db.relationship('User', backref='community_posts')
    group = db.relationship('Group', backref='community_posts')
class Community_Like(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('community_post.id'), primary_key=True)

    user = db.relationship('User', backref='likes')
    post = db.relationship('Community_post', backref='likes')
class Community_Dislike(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('community_post.id'), primary_key=True)

    user = db.relationship('User', backref='dislikes')
    post = db.relationship('Community_post', backref='dislikes')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)




    
     





# https://sqlalchemy-imageattach.readthedocs.io/en/1.0.0/guide/context.html#thumbnails

