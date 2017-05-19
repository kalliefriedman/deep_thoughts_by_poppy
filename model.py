"""Models and database functions for Audio Articles project."""

from os import environ
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library.
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

    @classmethod
    def save_tweet(cls, handle, tweet):
        """takes in twitter handle and tweet and adds user if doesn't exist"""
        user_id = cls.get_user_id(handle)
        if not user_id:
            new_user = cls(twitter_handle=handle)
            db.session.add(new_user)
            db.session.commit()
            user_object = cls.query.get(twitter_handle=handle).first()
            user_id = user_object.user_id
        PriorTweets.create_new_tweet(user_id, tweet)

    @classmethod
    def get_user_id(cls, handle):
        """takes in handle, returns user_id if user exists, else returns None"""
        user_object = cls.query.filter_by(twitter_handle=handle).first()
        print "yoyoyo"
        print user_object
        print user_object.user_id
        if user_object.user_id:
            user_id = user_object.user_id
            return user_id

    @classmethod
    def get_prior_tweets(cls, handle):
        """takes in a handle. if prior tweets, returns list of tweet content, else returns None."""
        user_id = cls.get_user_id(handle)
        print "heyheyhey"
        print user_id
        if user_id:
            prior_tweet_objects = PriorTweets.query.filter_by(user_id=user_id).all()
            prior_tweet_list = []
            for tweet in prior_tweet_objects:
                prior_tweet_list.append(tweet.tweet_content)
                print prior_tweet_list
            return prior_tweet_list
        else:
            return None


class PriorTweets(db.Model):
    """Prior generated tweets of particular users"""

    __tablename__ = "priortweets"

    tweet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    tweet_content = db.Column(db.String(200), nullable=False)

    user = db.relationship("User",
                           backref=db.backref("priortweets"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<tweet_id=%s user_id=%s tweet_content=%s" % (self.tweet_id, self.user_id, self.tweet_content))

    @classmethod
    def create_new_tweet(cls, user_id, tweet):
        """takes in user attributes and adds that user to database"""
        new_tweet = cls(user_id=user_id, tweet_content=tweet)
        db.session.add(new_tweet)
        db.session.commit()


##############################################################################
# Helper functions


def connect_to_db(app, db_uri=None):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or environ.get("DATABASE_URL", "postgresql:///tweet-generator")
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

