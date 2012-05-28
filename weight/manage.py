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

    add_user(u'admin', u'admin@localhost')

@manager.command
def add_user(username, email):
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
    

if __name__ == '__main__':
    manager.run()
