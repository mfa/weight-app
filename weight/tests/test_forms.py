from flask.testing import FlaskClient
import unittest

from main import db, app, DbUser
import models
from flask import session

from flask.ext.fillin import FormWrapper
from flask.ext.login import login_user
#from flask.ext.testing import TestCase

class FormTest(unittest.TestCase):

    username = u'testuser'
    password = u'testpassword'

    @classmethod
    def setUpClass(self):
        with app.test_request_context():
            db.create_all()
            u = models.User(username=self.username,
                            email=u'')
            u.set_password(self.password)
            db.session.add(u)
            db.session.commit()


    def test_login_ok(self):
        """ testing a correct login
        """
        with FlaskClient(app, response_wrapper=FormWrapper) as client:
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
        with FlaskClient(app, response_wrapper=FormWrapper) as client:
            response = client.get('/login', follow_redirects=True)

            response.form.fields['username'] = username
            response.form.fields['password'] = password
            response.form.fields['remember'] = False

            response = response.form.submit(client, follow_redirects=True)
            return response


    def test_login_fail(self):
        """ testing the login with wrong password
        """
        with app.test_request_context():
            response = self.login(self.username, u'wrong')
            self.assertEqual(response.status, '200 OK')
            self.assertNotEqual(session.get('user_id'), self.username)


    def test_weight_add(self):
        """ test adding one weight dataset
        """
        with FlaskClient(app, response_wrapper=FormWrapper) as client:

            self.login(self.username, self.password)
            with client.session_transaction() as sess:
                sess['user_id'] = self.username

            response = client.get('/weight/add/',
                                  follow_redirects=True)

            response.form.fields['weight'] = "10.0"

            response = response.form.submit(client)

            self.assertEqual(response.status, '200 OK')
