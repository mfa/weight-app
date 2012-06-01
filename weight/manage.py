#!/usr/bin/env python
from flask.ext.script import Manager
from main import app, db

# flask-Script
manager = Manager(app)

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

@manager.command
def createdb():
    """ Create Database (with initial user)
    """
    import models
    db.create_all()

    add_user(u'admin', email=get_emailaddress())

@manager.command
def add_user(username, email):
    """ Adds a User to the database with a random password and prints
        the random password.
    """
    from models import User
    if User.query.get(username):
        print("User %s already exists!" % username)
        return
    u = User(username=username, 
             email=email)
    pw = new_pw()
    u.set_password(pw)
    print("Password for %s set to: %s" % (username, pw))
    db.session.add(u)
    db.session.commit()

@manager.command
def import_from_xml(filename):
    from utils import import_weight_from_xml
    import_weight_from_xml(filename)


if __name__ == '__main__':
    manager.run()
