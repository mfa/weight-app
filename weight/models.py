""" Part of weight_app

    :copyright: (c) 2012 by Andreas Madsack.
    :license: BSD, see LICENSE for more details.
"""
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

    #: 
    fitbit_user_key = db.Column(db.String)
    fitbit_user_secret = db.Column(db.String)

    #: backref from Weight table
    weights = db.relationship('Weight',
                              backref='users',
                              lazy='select')

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

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<User %s %s>' % (self.username, self.email)


class Scale(db.Model):
    """ scales usable for weighting
    """

    #: given name of scale
    name = db.Column(db.UnicodeText,
                     unique=True, primary_key=True)

    #: owner of the scale
    owner = db.Column(db.UnicodeText)

    #: model and/or manufacturer
    model = db.Column(db.UnicodeText)

    #: comment for scale
    comment = db.Column(db.UnicodeText)


    #: backref from User table
    users = db.relationship('User',
                            backref='scales',
                            lazy='select',
                            cascade="all",
                            passive_updates=False)

    #: backref from Weight table
    weights = db.relationship('Weight',
                              backref='scales',
                              lazy='select',
                              cascade="all",
                              passive_updates=False)

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
    """ Weights for day and user with a given scale
    """

    id = db.Column(db.Integer, db.Sequence('weight_id_seq'),
                   unique=True, primary_key=True)

    #: date of weighing
    wdate = db.Column(db.Date(),
                     db.DefaultClause(db.func.sysdate()),
                     nullable=False)

    #: allow only one entry per day and user
    #: FIXME: looks like it doesn't work with sqlite?
    db.UniqueConstraint('wdate', 'user_username',
                        name='weight_date_user_unique')

    #: day of week
    @property
    def weekday(self):
        dt = self.wdate
        return dt.strftime("%a")

    #: scale used for weighting
    scale_name = db.Column(db.UnicodeText,
                           db.ForeignKey("scale.name"))

    #: weight of user at given day
    weight = db.Column(db.Float)

    #: weighted user
    user_username = db.Column(db.UnicodeText,
                              db.ForeignKey("user.username"))

    #: comment for this weighting
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
