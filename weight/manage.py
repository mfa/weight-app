#!/usr/bin/env python
""" Part of weight_app

    :copyright: (c) 2012 by Andreas Madsack.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.script import Manager
from main import create_app, db

from utils import new_pw, get_emailaddress

# flask-Script
manager = Manager(create_app)

@manager.command
def createdb():
    """ Create Database (with initial user)
    """
    import models
    db.create_all()

    add_user(u'admin', email=get_emailaddress())

@manager.command
def add_user(username, email, quiet=False):
    """ Adds a User to the database with a random password and prints
        the random password.
    """
    from models import User
    if User.query.get(username):
        print("User %s already exists!" % username)
        return
    u = User(username=username, 
             email=email.strip())
    pw = new_pw()
    u.set_password(pw)
    if not quiet:
        print("Password for %s set to: %s" % (username, pw))
    db.session.add(u)
    db.session.commit()

@manager.command
def import_from_xml(filename, username):
    from utils import import_weight_from_xml
    import_weight_from_xml(filename, username)


if __name__ == '__main__':
    manager.run()
