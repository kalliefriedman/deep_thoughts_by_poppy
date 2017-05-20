from flask import (Flask, Response, render_template, redirect, request
                   session, jsonify)
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

    def testLogin(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn("Poppy")


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

