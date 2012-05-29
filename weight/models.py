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

    #: firstname (not required)
    firstname = db.Column(db.UnicodeText, nullable=True)

    #: lastname (not required)
    lastname = db.Column(db.UnicodeText, nullable=True)

    #: default scale of this user
    default_scale_id = db.Column(db.UnicodeText,
                                 db.ForeignKey(scale.id))

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


class Scale(db.Model):
    """
    """

    #:
    id = db.Column(db.UnicodeText,
                   unique=True, primary_key=True)

    #:
    owner = db.Column(db.UnicodeText)

    #:
    model = db.Column(db.UnicodeText)

    #:
    comment = db.Column(db.UnicodeText)


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


class Weight(db.Model):
    """
    """

    id = db.Column(db.Integer, db.Sequence(),
                   unique=True, primary_key=True)

    #: date of weighing
    date = db.Column(db.Date(timezone=True),
                     db.DefaultClause(db.func.today()),
                     nullable=False)

    #: day of week (as string), could be an enum
    weekday = db.Column(db.UnicodeText)

    #:
    scale_id = db.Column(db.UnicodeText,
                         db.ForeignKey(scale.id))

    #:
    weight = db.Column(db.Float)

    #:
    comment = db.Column(db.UnicodeText)

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
