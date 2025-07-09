import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timedelta
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    posts = relationship('Post', backref='author')
    comments = relationship('Comment', backref='author')
    followers = relationship('Follower', foreign_keys='Follower.user_id', backref='user')
    following = relationship('Follower', foreign_keys='Follower.follower_id', backref='follower')
    likes = relationship('Like', backref='user')
    stories = relationship('Story', backref='user')
    sent_messages = relationship('Message', foreign_keys='Message.sender_id', backref='sender')
    received_messages = relationship('Message', foreign_keys='Message.receiver_id', backref='receiver')
    saved_posts = relationship('SavedPost', backref='user')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    image_url = Column(String(250), nullable=False)
    caption = Column(String(2200))
    timestamp = Column(DateTime, default=datetime.utcnow)

    comments = relationship('Comment', backref='post')
    likes = relationship('Like', backref='post')
    saved_by = relationship('SavedPost', backref='post')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    text = Column(String(500), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    follower_id = Column(Integer, ForeignKey('user.id'))

class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Story(Base):
    __tablename__ = 'story'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    media_url = Column(String(250), nullable=False)
    caption = Column(String(300))
    timestamp = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=24))

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    content = Column(String(1000), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SavedPost(Base):
    __tablename__ = 'saved_post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    saved_at = Column(DateTime, default=datetime.utcnow)

def draw_er():
    try:
        result = render_er(Base, 'diagram.png')
        print("Diagrama generado correctamente")
    except Exception as e:
        print("Error al generar el diagrama")
        raise e

draw_er()
