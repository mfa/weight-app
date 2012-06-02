from flask.ext.wtf import Form, TextField, PasswordField, SubmitField, \
     HiddenField, Required, BooleanField, ValidationError, validators, \
     Optional, EqualTo, DateField, FloatField

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
    submit = SubmitField("Save")

 


class WeightForm(Form):
    weight = FloatField("Weight", )
    wdate = DateField("Date", default=datetime.date.today())
    comment = TextField("Comment", [Optional()])
    # set scale

    wid = HiddenField()
    submit = SubmitField("Save")


class Scale(Form):
    pass


