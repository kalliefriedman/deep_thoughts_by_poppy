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
            user_object = cls.query.filter_by(twitter_handle=handle).first()
            user_id = user_object.user_id
        PriorTweets.create_new_tweet(user_id, tweet)

    @classmethod
    def get_user_id(cls, handle):
        """takes in handle, returns user_id if user exists, else returns None"""
        user_object = cls.query.filter_by(twitter_handle=handle).first()
        if user_object:
            user_id = user_object.user_id
            return user_id

    @classmethod
    def get_prior_tweets(cls, handle):
        """takes in a handle. if prior tweets, returns list of tweet content, else returns None."""
        user_id = cls.get_user_id(handle)
        if user_id:
            prior_tweet_objects = PriorTweets.query.filter_by(user_id=user_id).all()
            prior_tweet_list = []
            for tweet in prior_tweet_objects:
                prior_tweet_list.append(tweet.tweet_content)
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


def example_data_users():
    """creates sample users"""
    realDonaldTrump = User(twitter_handle='realDonaldTrump')
    db.session.add(realDonaldTrump)

    KimKardashian = User(twitter_handle='KimKardashian')
    db.session.add(KimKardashian)

    db.session.commit()


def example_data_prior_tweets():
    """creates sample tweets"""
    tweet1 = User(user_id='1', tweet_content='eat pray love my dog')
    db.session.add(tweet1)

    tweet2 = User(user_id='1', tweet_content='like to sleep and nap and book and work and live and collar and cookie')
    db.session.add(tweet2)

    tweet3 = User(user_id='1', tweet_content='food desk lamp chair fence sprayerbottle Friday!!')
    db.session.add(tweet3)

    tweet4 = User(user_id='1', tweet_content='suitcase going on a trip chair like that decanter')
    db.session.add(tweet4)

    tweet5 = User(user_id='1', tweet_content='why poppy #heart book purse')
    db.session.add(tweet5)

    tweet6 = User(user_id='2', tweet_content='salt pepper, orchid, happy happiness')
    db.session.add(tweet6)

    tweet7 = User(user_id='2', tweet_content='love my life!')
    db.session.add(tweet7)

    tweet8 = User(user_id='2', tweet_content='heart eat water! gum paper')
    db.session.add(tweet8)

    db.session.commit()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."

