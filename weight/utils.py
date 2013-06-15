""" Part of weight_app

    :copyright: (c) 2012 by Andreas Madsack.
    :license: BSD, see LICENSE for more details.
"""
from models import Scale, Weight, User
from main import db
from lxml import etree
import datetime
import fitbit

def import_weight_from_xml(filename, username=None):
    """ Import Scales and Weight from my own old xml-Data
    """

    def add_scales(doc, username):
        for elem in doc.xpath("//scales/item"):
            sc1 = Scale(name=unicode(elem.attrib["id"]))
            for i in elem:
                if i.tag=='owner':
                    sc1.owner = unicode(i.text)
                if i.tag=='model' and i.text:
                    sc1.model = unicode(i.text)
            db.session.add(sc1)
            db.session.flush()
            if 'default' in elem.attrib and \
                    elem.attrib['default'] == "True" and username:
                u1 = User.query.get(username)
                u1.default_scale_name = sc1.name
        db.session.commit()

    def add_weight(doc, username):
        if username:
            u1 = User.query.get(username)
        for elem in doc.xpath('//days/day'):
            we1 = Weight()
            we1.wdate = datetime.datetime.strptime(elem.attrib['date'],
                                                   '%Y-%m-%d')
            if u1:
                we1.user_username = u1.username
            w = False
            for i in elem:
                if i.tag=='weight' and i.text:
                    if 'scale' in i.attrib:
                        sc1 = Scale.query.get(unicode(i.attrib['scale']))
                        if sc1:
                            we1.scale_name = sc1.name
                    we1.weight = unicode(i.text)
                    w = True
                if i.tag=='comment' and i.text:
                    we1.comment = unicode(i.text)
            if w:
                db.session.add(we1)
        db.session.commit()
                
    doc = etree.parse(filename)
    add_scales(doc, username)
    add_weight(doc, username)

def new_pw():
    """ Generate a new password with letters and digits
    """
    import string
    import random
    return "".join(random.sample(string.letters + string.digits, 8))

def get_emailaddress():
    import subprocess
    m = subprocess.Popen('git config --get user.email',
                         shell=True, stdout=subprocess.PIPE).stdout
    email = unicode(m.read())
    if '@' not in email:
        email = None
    return email

def fitbit_push(user, wdate, weight):
    # import credentials from extra file:
    from credentials import APP_KEY, APP_SECRET, USER_KEY, USER_SECRET
    # to get USER_KEY and USER_SECRET see
    # http://python-fitbit.readthedocs.org/en/latest/

    fb = fitbit.Fitbit(APP_KEY, APP_SECRET,
                       user_key=user.fitbit_user_key,
                       user_secret=user.fitbit_user_secret)
    fb.body(date=wdate, data={'weight': weight})
