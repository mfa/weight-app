from flask.testing import FlaskClient
import unittest

from main import db, app, DbUser
import models
from flask import session

from flask.ext.fillin import FormWrapper
#from flask.ext.testing import TestCase

class FormTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        with app.test_request_context():
            db.create_all()
            u = models.User(username=u'testuser', 
                            email=u'')
            pw = u'testpassword'
            u.set_password(pw)
            db.session.add(u)
            db.session.commit()

    def test_login_ok(self):
        """ 
        """
        from flask.ext.login import login_user

        with FlaskClient(app, response_wrapper=FormWrapper) as client:
            response = client.get('/login')

            username = u'testuser'
            response.form.fields['username'] = username
            response.form.fields['password'] = u'testpassword'
            response.form.fields['remember'] = False

            response = response.form.submit(client)

            self.assertEqual(response.status, '302 FOUND')
            self.assertEqual(session.get('user_id'), username)


    def test_login_fail(self):
        """ 
        """
        from flask.ext.login import login_user

        with FlaskClient(app, response_wrapper=FormWrapper) as client:
            response = client.get('/login')

            username = u'testuser'
            response.form.fields['username'] = username
            response.form.fields['password'] = u'wrong'
            response.form.fields['remember'] = False

            response = response.form.submit(client)

            self.assertEqual(response.status, '200 OK')
            self.assertNotEqual(session.get('user_id'), username)
