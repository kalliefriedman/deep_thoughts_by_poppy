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
    """Twitter user we are generating tweets for"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    twitter_handle = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<User user_id=%s twitter_handle=%s" % (self.user_id, self.twitter_handle))


    # @classmethod
    # def create_new_user(cls, username, f_name, l_name, password, email,
    #                     phone, password_salt):
    #     """takes in user attributes and adds that user to database"""
    #     new_user = cls(username=username, f_name=f_name, l_name=l_name, password=password, email=email,
    #                    phone=phone, password_salt=password_salt)
    #     db.session.add(new_user)
    #     db.session.commit()

    # @classmethod
    # def get_user_object_by_user_id(cls, user_id):
    #     """takes in a userID and returns first user with that userID"""
    #     user_object = cls.query.filter_by(user_id=user_id).first()
    #     return user_object

class PriorTweets(db.Model):
    """Prior generated tweets of particular users"""

    __tablename__ = "users"

    tweet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    tweet_content = db.Column(db.String(200), nullable=False)

    priortweets = db.relationship("PriorTweets",
                           backref=db.backref("user"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<tweet_id=%s user_id=%s tweet_content=%s" % (self.tweet_id, self.user_id, self.tweet_content))
##############################################################################
# Helper functions


def connect_to_db(app, db_uri=None):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or environ.get("DATABASE_URL", "postgresql:///audioarticles")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


# def example_data_users():
#     """creating and adding sample users"""
#     kallie = User(username='kfriedman', f_name='Kallie', l_name='Friedman',
#                   password='password', password_salt='salt',
#                   email='kallie@yahoo.com')
#     db.session.add(kallie)

#     natalie = User(username='nfriedman', f_name='Natalie', l_name='Friedman',
#                    password='password', password_salt='salt',
#                    email='natalie@hotmail.com')
#     db.session.add(natalie)

#     randy = User(username='rfriedman', f_name='Randy', l_name='Friedman',
#                  password='password', password_salt='salt',
#                  email='randy@yahoo.com')
#     db.session.add(randy)

#     db.session.commit()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."

