from main import db
import hashlib

class User(db.Model):
    """ simple User model with password (md5 hashed) and email.
    """

    #: username (unicode)
    username = db.Column(db.UnicodeText, primary_key=True, unique=True)
    
    #: password (saved using md5)
    password = db.Column(db.String)

    #: email address
    email = db.Column(db.UnicodeText)

    # firstname (not required)
    firstname = db.Column(db.UnicodeText, nullable=True)

    # lastname (not required)
    lastname = db.Column(db.UnicodeText, nullable=True)

    #: creation date, set on creation
    createdate = db.Column(db.DateTime(timezone=True),
                           db.DefaultClause(db.func.now()),
                           nullable=False)
    #: modification date, set on every change
    lastmoddate = db.Column(db.DateTime(timezone=True),
                            db.DefaultClause(db.func.now()),
                            nullable=False)
    #: changed_by
    changed_by = db.Column(db.UnicodeText,
                           db.DefaultClause(db.func.session_user()))

    def set_password(self, pw):
        cpw = hashlib.md5(pw)
        self.password = cpw.hexdigest()

    def check_password(self, pw):
        cpw = hashlib.md5(pw)
        if self.password == cpw.hexdigest():
            return True
        else:
            return False

    def __repr__(self):
        return '<User %s %s>' % (self.username, self.email)
