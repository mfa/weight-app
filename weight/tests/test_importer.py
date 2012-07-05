""" Part of weight_app

    :copyright: (c) 2012 by Andreas Madsack.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.testing import TestCase
from flask import Flask
import datetime

from main import db, create_app
import models

import utils
import StringIO

def add_some_data(username):
    # add testuser
    u1 = models.User(username=username)
    u1.set_password(utils.new_pw())
    db.session.add(u1)
    db.session.flush()
    db.session.commit()

    xdata = StringIO.StringIO(u"<w>"
                              "<scales><item id=\"sid1\">"
                              "<owner>o1</owner>"
                              "<model>m1</model>"
                              "</item></scales>"
                              "<days><day date=\"2012-06-03\">"
                              "<weight scale=\"sid1\">50.1</weight>"
                              "</day></days>"
                              "</w>")
    utils.import_weight_from_xml(xdata, username)


class ImportTest(TestCase):

    username = u'user1'

    def setUp(self):
        db.create_all()
        with self.app.test_request_context():
            add_some_data(username=self.username)

    def create_app(self):
        return create_app()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_scale_1(self):
        """ is the id imported?
        """
        with self.app.test_request_context():
            sc1 = models.Scale.query.get(u'sid1')
            self.assertNotEqual(sc1, None)

    def test_scale_2(self):
        """ query the imported dataset
        """
        with self.app.test_request_context():
            sc1 = models.Scale.query.get(u'sid1')
            self.assertEqual(sc1.owner, u'o1')
            self.assertEqual(sc1.model, u'm1')

    def test_weight_1(self):
        """ count data in weight table
        """
        with self.app.test_request_context():
            we1 = models.Weight.query.all()
            self.assertNotEqual(we1[0], None)

    def test_weight_2(self):
        """ query the imported dataset
        """
        with self.app.test_request_context():
            wx = datetime.datetime.strptime('2012-06-03',
                                            '%Y-%m-%d').date()
            we1 = models.Weight.query.filter_by(wdate=wx).all()
            self.assertEqual(len(we1), 1)
            we1 = we1[0]
            sc1 = models.Scale.query.get(u'sid1')
            self.assertEqual(we1.wdate, wx)
            self.assertEqual(we1.weight, 50.1)
            self.assertEqual(we1.scales, sc1)

    def test_weight_3(self):
        """ add some data
        """
        with self.app.test_request_context():
            wx = datetime.datetime.strptime('2012-06-04',
                                            '%Y-%m-%d').date()
            we1 = models.Weight(wdate=wx)
            we1.weight=10
            sc1 = models.Scale.query.get(u'sid1')
            we1.scale_name = sc1.name
            u1 = models.User.query.get(u'user1')
            we1.user_username = u1.username

            db.session.add(we1)
            db.session.flush()

            self.assertEqual(we1.wdate, wx)
            self.assertEqual(we1.weight, 10)
            self.assertEqual(we1.scales, sc1)
            self.assertEqual(we1.user_username, u1.username)

    def test_import_1(self):
        """ empty weight field is ignored on import => no dataset
        """
        with self.app.test_request_context():
            xdata = StringIO.StringIO(u"<w>"
                                      "<days><day date=\"2012-06-02\">"
                                      "</day></days>"
                                      "</w>")
            utils.import_weight_from_xml(xdata, u'user1')
            wx = datetime.datetime.strptime('2012-06-02',
                                            '%Y-%m-%d').date()
            we1 = models.Weight.query.filter_by(wdate=wx).all()
            self.assertEqual(len(we1), 0)


    def test_import_2(self):
        """ import without scale set. scales should be None.
        """
        with self.app.test_request_context():
            xdata = StringIO.StringIO(u"<w>"
                                      "<days><day date=\"2012-06-02\">"
                                      "<weight>10</weight>"
                                      "</day></days>"
                                      "</w>")
            utils.import_weight_from_xml(xdata, u'user1')
            wx = datetime.datetime.strptime('2012-06-02',
                                            '%Y-%m-%d').date()
            we1 = models.Weight.query.filter_by(wdate=wx).all()
            self.assertEqual(len(we1), 1)
            self.assertEqual(we1[0].scales, None)
