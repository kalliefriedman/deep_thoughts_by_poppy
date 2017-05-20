import sys
import twitter
from random import choice
from os import environ
from jinja2 import StrictUndefined
from flask import (Flask, render_template, request,
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from model import User, PriorTweets, connect_to_db, db

app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
# Normally, if you use an undefined variable in Jinja2, it fails
# silently. That is bad. This will fix it.
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=["GET"])
def index():
    """Renders homepage"""
    return render_template("homepage.html")


@app.route('/generate-new-tweet.json', methods=["POST"])
def make_new_tweet():
    """Reads in the user's timeline of tweets, and returns a new tweet"""
    handle = request.form.get("handle")
    if handle:
        api = twitter.Api(
            consumer_key=environ['TWITTER_CONSUMER_KEY'],
            consumer_secret=environ['TWITTER_CONSUMER_SECRET'],
            access_token_key=environ['TWITTER_ACCESS_TOKEN_KEY'],
            access_token_secret=environ['TWITTER_ACCESS_TOKEN_SECRET'])
        statuses = api.GetUserTimeline(user_id=None, screen_name=handle,
                                       since_id=None, max_id=None, count=200,
                                       include_rts=True, trim_user=False,
                                       exclude_replies=False)
        markov_input = ""
        if statuses:
            for status in statuses:
                markov_input += status.text
                markov_input += " "
            # create a dictionary of key value pairs with the markov_input
            markov_pairings = make_chains(markov_input)
            # create a new markov chain using the markov_pairings dictionary
            newtweet = generate_text(markov_pairings)

            User.save_tweet(handle, newtweet)

            return jsonify(newtweet)
        else:
            return jsonify(None)
    else:
        return jsonify(None)


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""
    chains = {}
    words = text_string.split()

    for index in range(0, len(words)-2):
        word1, word2, word3 = words[index], words[index + 1], words[index + 2]
        key, value = tuple([word1, word2]), word3
        if key in chains:
            chains[key].append(value)
        else:
            chains[key] = [word3]

    return chains


def generate_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    output_text = ""

    # make key list and then choose the first key randomly
    keys = chains.keys()
    new_key = choice(keys)

    # add the first tuple key to the output_text
    output_text = output_text + new_key[0] + " " + new_key[1] + " "
   
    # continues to add keys until text is too long or the key isn't in dict
    while len(output_text) < 130:
        value = chains.get(new_key, None)
        if value:
            random_value = choice(value)
        else:
            break
        output_text += (random_value+" ")
        new_key = tuple([new_key[1], random_value])

    return output_text


@app.route('/get-past-tweets.json', methods=["GET"])
def get_prior_tweets():
    """Takes in a username and returns their prior tweets (if they exist)"""
    handle = request.args.get("handle")
    prior_tweets = User.get_prior_tweets(handle)
    return jsonify(prior_tweets)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=int(environ.get("PORT", 5000)), host='0.0.0.0')
