""" Part of weight_app

    :copyright: (c) 2012 by Andreas Madsack.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.testing import TestCase
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask

from main import create_app, db
import models

class BaseTest(TestCase):

    def setUp(self):
        db.create_all()

    def create_app(self):
        return create_app()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

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
        from manage import add_user
        add_user(u'foo', u'foo@example.com', quiet=True)
        us1 = models.User.query.get(u'foo')
        self.assertEqual(u'foo', us1.username)

