""" Part of weight_app

    :copyright: (c) 2012 by Andreas Madsack.
    :license: BSD, see LICENSE for more details.
"""
from flask.testing import FlaskClient
from flask import Flask

from main import db, DbUser, create_app
import models
from flask import session

from flask.ext.fillin import FormWrapper
from flask.ext.login import login_user
from flask.ext.testing import TestCase

class FormTest(TestCase):

    username = u'testuser'
    password = u'testpassword'

    def setUp(self):
        db.create_all()
        with self.app.test_request_context():
            u = models.User(username=self.username,
                            email=u'')
            u.set_password(self.password)
            db.session.add(u)
            db.session.commit()

    def create_app(self):
        return create_app()

    def create_app(self):
        return create_app()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_ok(self):
        """ testing a correct login
        """
        with FlaskClient(self.app, response_wrapper=FormWrapper) as client:
            response = client.get('/login', follow_redirects=True)

            response.form.fields['username'] = self.username
            response.form.fields['password'] = self.password
            response.form.fields['remember'] = False

            response = response.form.submit(client)
            self.assertEqual(response.status, '302 FOUND')
            # because of session self.login can't be used
            self.assertEqual(session.get('user_id'), self.username)


    def login(self, username, password):
        """ login to site with username and password;
        """
        with FlaskClient(self.app, response_wrapper=FormWrapper) as client:
            response = client.get('/login', follow_redirects=True)

            response.form.fields['username'] = username
            response.form.fields['password'] = password
            response.form.fields['remember'] = False

            response = response.form.submit(client, follow_redirects=True)
            return response


    def test_login_fail(self):
        """ testing the login with wrong password
        """
        with self.app.test_request_context():
            response = self.login(self.username, u'wrong')
            self.assertEqual(response.status, '200 OK')
            self.assertNotEqual(session.get('user_id'), self.username)

    def test_weight_add(self):
        """ test adding one weight dataset
        """
        with FlaskClient(self.app, response_wrapper=FormWrapper) as client:

            self.login(self.username, self.password)
            with client.session_transaction() as sess:
                sess['user_id'] = self.username

            response = client.get('/weight/add/',
                                  follow_redirects=True)
            response.form.fields['weight'] = "10.0"
            response = response.form.submit(client)

            self.assertEqual(response.status, '200 OK')

    def test_scale_add(self):
        """ test adding one scale dataset
        """
        with FlaskClient(self.app, response_wrapper=FormWrapper) as client:

            self.login(self.username, self.password)
            with client.session_transaction() as sess:
                sess['user_id'] = self.username

            response = client.get('/scale/add/',
                                  follow_redirects=True)
            response.form.fields['name'] = "testscale1"
            response.form.fields['owner'] = "testowner1"
            response = response.form.submit(client)

            self.assertEqual(response.status, '200 OK')

    def test_scale_edit(self):
        """ test editing one scale dataset
        """
        sc1 = models.Scale.query.get(u'sid1')
        # insert scale for editing later
        if not sc1:
            sc1 = models.Scale(name=u'sid1')
            db.session.add(sc1)
            db.session.commit()
        with FlaskClient(self.app, response_wrapper=FormWrapper) as client:

            self.login(self.username, self.password)
            with client.session_transaction() as sess:
                sess['user_id'] = self.username

            response = client.get('/scale/sid1/',
                                  follow_redirects=True)
            response.form.fields['owner'] = "testowner2"
            response = response.form.submit(client)

            self.assertEqual(response.status, '200 OK')

        with self.app.test_request_context():
            sc = models.Scale.query.get(u'sid1')
            self.assertEqual(sc.owner, u'testowner2')

    def test_profile_edit(self):
        """ test editing the user profile
        """
        sc1 = models.Scale.query.get(u'sid1')
        # insert scale for editing later
        if not sc1:
            sc1 = models.Scale(name=u'sid1')
            db.session.add(sc1)
            db.session.commit()
        with FlaskClient(self.app, response_wrapper=FormWrapper) as client:

            self.login(self.username, self.password)
            with client.session_transaction() as sess:
                sess['user_id'] = self.username

            # dataset was added with the importertests
            response = client.get('/profile',
                                  follow_redirects=True)
            response.form.fields['firstname'] = u"firstname1"
            response.form.fields['default_scale'] = u"sid1"
            response = response.form.submit(client)

            self.assertEqual(response.status, '200 OK')

        with self.app.test_request_context():
            u1 = models.User.query.get(self.username)
            self.assertEqual(u1.firstname, u'firstname1')
            self.assertEqual(u1.default_scale_name, u'sid1')
