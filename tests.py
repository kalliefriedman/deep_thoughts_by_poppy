from flask import Flask, Response, render_template, redirect, request, session, jsonify
import unittest
from server import app
from model import db, connect_to_db, example_data_users, example_data_prior_tweets


class TestHomepage(unittest.TestCase):
    """Tests for homepage"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()

    def tearDown(self):
        """Should close the session and drop all tables"""
        db.session.close()
        db.drop_all()

    def testInitalHomepage(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Deep thoughts by Poppy...", result.data)

    def testGenerateNewTweet(self):
        result = self.client.post('generate-new-tweet.json', data={'handle': "realDonaldTrump"})
        self.assertEqual(result.status_code, 200)


class TestDatabase(unittest.TestCase):
    """Tests to ensure database is working as expected"""

    def setUp(self):
        """What needs to be done prior to each test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data_users()
        example_data_prior_tweets()

    def tearDown(self):
        """Do at end of every test."""
        db.session.close()
        db.drop_all()

    def testGetPriorTweets(self):
        result = self.client.get('/get-past-tweets.json', query_string={'handle': "realDonaldTrump"})
        self.assertEqual(result.status_code, 200)
        self.assertIn("eat pray", result.data)
        self.assertIn("why poppy", result.data)

    def testGetPriorTweetsNoPrior(self):
        result = self.client.get('/get-past-tweets.json', query_string={'handle': "BarakObama"})
        self.assertIn("null", result.data)

if __name__ == "__main__":
    unittest.main()
