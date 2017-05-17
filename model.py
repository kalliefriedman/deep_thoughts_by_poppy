"""Models and database functions for Audio Articles project."""


from os import environ
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

##############################################################################
# Model definitions


class User(db.Model):
    """User of Audio Articles app."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    password_salt = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=True)

# four way relationship from users table over to tags table, stepping through taggingss and articles
    tags = db.relationship("Tag",
                           primaryjoin='User.user_id == Article.user_id',
                           secondary='join(Article, Tagging, Article.article_id == Tagging.article_id)',
                           secondaryjoin='Tagging.tag_id == Tag.tag_id',
                           viewonly=True,
                           backref=db.backref("users"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<User user_id=%s username=%s f_name=%s l_name=%s email=%s phone=%s>>" % (self.user_id, self.username, self.f_name,
                self.l_name, self.email, self.phone))

    @classmethod
    def get_user_object_by_email(cls, input_email):
        """Takes in an input email and returns first user with that email"""
        user_by_email = cls.query.filter_by(email=input_email).first()
        return user_by_email

    @classmethod
    def get_user_object_by_username(cls, input_username):
        """takes in username and returns first user with that username"""
        user_by_username = cls.query.filter_by(username=input_username).first()
        return user_by_username

    @classmethod
    def create_new_user(cls, username, f_name, l_name, password, email,
                        phone, password_salt):
        """takes in user attributes and adds that user to database"""
        new_user = cls(username=username, f_name=f_name, l_name=l_name, password=password, email=email,
                       phone=phone, password_salt=password_salt)
        db.session.add(new_user)
        db.session.commit()

    @classmethod
    def get_user_object_by_user_id(cls, user_id):
        """takes in a userID and returns first user with that userID"""
        user_object = cls.query.filter_by(user_id=user_id).first()
        return user_object