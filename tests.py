from flask import (Flask, Response, render_template, redirect, request, flash,
                   session, jsonify)
import unittest
from server import app, session
from model import db, connect_to_db, example_data_users, example_data_articles, example_data_tags, example_data_taggings


class TestLoggedOut(unittest.TestCase):
    """Tests for audio articles site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
      