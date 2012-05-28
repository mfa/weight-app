from flask.ext.script import Manager
from main import app, db
import os

# flask-Script
manager = Manager(app)

def new_pw():
    import string
    import random
    return "".join(random.sample(string.letters+string.digits, 8))

@manager.command
def createdb():
    """ Create Database (with initial user)
    """
    from models import User
    db.create_all()

    u = User(username=u'admin', 
             email=u'admin@localhost')
    pw = new_pw()
    u.set_password(pw)
    print("Password for admin set to: %s" % pw)
    db.session.add(u)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
