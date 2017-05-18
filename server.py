import sys
from random import choice
from os import environ
from jinja2 import StrictUndefined
from flask import (Flask, Response, render_template, flash, redirect, request,
                   session, jsonify)
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
    """Renders homepage if user isn't logged in. Otherwise redirects user to user-articles."""
    return render_template("homepage.html")

@app.route('/generate-new-tweet.json', methods=["POST"])
    def make_new_tweet():
    """Reads in the user's timeline of tweets, and returns a new tweet and previously generated tweets (if they exist)"""
    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
#     call to twitter API
#     if user doesn't exist or isn't public:
#      return a flash message and reload homepage
#     if there is a response, read in that data
#     then, generate a tweet, store that new tweet, send over that object to template

@app.route('/get-past-tweets.json', methods=["GET"])
    
#     if user id exists in database, return that list of tweets to template to display


# chains = {}  # dictionary for all the texts going through


# def open_and_read_file(file_path):
#     """Takes file path as string; returns text as string.
#     Takes a string that is a file path, opens the file, and turns
#     the file's contents as one string of text.
#     """

#     open_file = open(file_path)
#     return open_file.read()


# def make_chains(text_string, chains):
#     """Takes input text as string; returns _dictionary_ of markov chains.
#     A chain will be a key that consists of a tuple of (word1, word2)
#     and the value would be a list of the word(s) that follow those two
#     words in the input text.
#     For example:
#         >>> make_chains("hi there mary hi there juanita")
#         {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
#     """

#     words = text_string.split()

#     # Solution 2
#     for index in range(0, len(words)-2):
#         key = tuple([words[index], words[index+1]])
#         chains.setdefault(key, []).append(words[index+2])
#     chains.setdefault((words[-2], words[-1]), []).append(None)

#     return chains


# def make_text(chains):
#     """Takes dictionary of markov chains; returns random text."""

#     output_text = ""

#     # made key list and then choise the first key random
#     keys = chains.keys()
#     new_key = choice(keys)

#     # add the first tuple key to the output_text
#     output_text = output_text + new_key[0] + " " + new_key[1]

#     # from index 2 to end which is none, the code runs
#     while True:
#         random_value = choice(chains[new_key])
#         if random_value is None:
#             break
#         output_text += " %s" % random_value
#         new_key = tuple([new_key[1], random_value])

#     return output_text


# def combine_texts(argv):
#     """Reads in arbitrary number of texts files and adds them to our dictionary."""

#     # split the argv
#     texts_to_add = sys.argv[1:]

#     for text in texts_to_add:
#         input_text = open_and_read_file(text)
#         make_chains(input_text, chains)

# # Produce random text
# combine_texts(sys.argv)
# random_text = make_text(chains)
# print random_text


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=int(environ.get("PORT", 5000)), host='0.0.0.0')
