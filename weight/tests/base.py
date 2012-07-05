""" Part of weight_app

    :copyright: (c) 2012 by Andreas Madsack.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.testing import TestCase
from flask import Flask
import unittest

#from main import db, app
from main import db
import models

class BaseTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        db.create_all()
        return app

    def test_get_emailaddress(self):
        from utils import get_emailaddress
        em = get_emailaddress()
        self.assertIn(u'@', em)

    def test_new_pw(self):
        from utils import new_pw
        pw = new_pw()
        self.assertEqual(len(pw), 8)
        self.assertTrue(pw.isalnum())

    def test_add_user(self):
        with self.app.test_request_context():
            from manage import add_user
            add_user(u'foo', u'foo@example.com', quiet=True)
            us1 = models.User.query.get(u'foo')
            self.assertEqual(u'foo', us1.username)

