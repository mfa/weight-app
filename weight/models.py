from main import db
import hashlib
from sqlalchemy.orm import column_property
import datetime

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
    default_scale_name = db.Column(db.UnicodeText,
                                   db.ForeignKey("scale.name"))

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
    name = db.Column(db.UnicodeText,
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

    def __repr__(self):
        return '<Scale %s %s>' % (self.name, self.owner)


class Weight(db.Model):
    """
    """

    id = db.Column(db.Integer, db.Sequence('weight_id_seq'),
                   unique=True, primary_key=True)

    #: date of weighing
    wdate = db.Column(db.Date(timezone=True),
                     db.DefaultClause(db.func.sysdate()),
                     nullable=False)

    #: allow only one entry per day and user
    db.UniqueConstraint('wdate', 'user_username',
                        name='weight_date_user_unique')

    #: day of week
    @property
    def weekday(self):
        dt = self.wdate
        return dt.strftime("%a")

    #:
    scale_name = db.Column(db.UnicodeText,
                           db.ForeignKey("scale.name"))

    #:
    weight = db.Column(db.Float)

    #:
    user_username = db.Column(db.UnicodeText,
                              db.ForeignKey("user.username"))

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

    def __repr__(self):
        return '<Weight %s %s>' % (str(self.wdate), self.user_username)
