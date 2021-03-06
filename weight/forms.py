""" Part of weight_app

    :copyright: (c) 2012 by Andreas Madsack.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.wtf import Form, TextField, PasswordField, SubmitField, \
     HiddenField, Required, BooleanField, ValidationError, validators, \
     Optional, EqualTo, DateField, FloatField, SelectField

from flask import request
import datetime

class LoginForm(Form):
    """The default login form"""

    username = TextField("Username", validators=[
            Required(message="Username missing")])
    password = PasswordField("Password", validators=[
            Required(message="Password not provided")])
    remember = BooleanField("Remember Me", default=True)
    next = HiddenField()
    submit = SubmitField("Login")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.next.data = request.args.get('next', None)

    def validate_password(form, field):
        from models import User
        u1 = User.query.get(form.username.data)
        if u1:
            if not u1.check_password(field.data):
                raise ValidationError('Username or Password wrong')
        else:
            raise ValidationError('Username or Password wrong')


class ProfileForm(Form):
    """ Form for editing User data
    """
    firstname = TextField("Firstname")
    lastname = TextField("Lastname")
    email = TextField("Email", [validators.Email(), Optional()])
    # set default scale
    password = PasswordField('New Password',
                             [EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')

    default_scale = SelectField(u'Default Scale')

    submit = SubmitField("Save")

 
class WeightForm(Form):
    """ Form for editing and adding weight data
    """
    weight = FloatField("Weight", )
    wdate = DateField("Date", default=datetime.date.today())
    comment = TextField("Comment", [Optional()])
    scale_name = SelectField(u'Scale')

    wid = HiddenField()
    submit = SubmitField("Save")


class ScaleForm(Form):
    """ Form for editing and adding scales
    """
    name = TextField("Name", )
    owner = TextField("Owner", [Optional()])
    model = TextField("Model", [Optional()])
    comment = TextField("Comment", [Optional()])

    sid = HiddenField()
    submit = SubmitField("Save")


