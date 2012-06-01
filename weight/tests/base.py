from flask.ext.testing import TestCase
from flask import Flask
import unittest

from main import db, app
import models

class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        db.create_all()

    def test_get_emailaddress(self):
        from utils import get_emailaddress
        em = get_emailaddress()
        self.assertIn(u'@', em)

    def test_ass_user(self):
        with app.test_request_context():
            from manage import add_user
            add_user(u'foo', u'foo@example.com', quiet=True)
            us1 = models.User.query.get(u'foo')
            self.assertEqual(u'foo', us1.username)

