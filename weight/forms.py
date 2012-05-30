from flask.ext.wtf import Form, TextField, PasswordField, SubmitField, \
     HiddenField, Required, BooleanField, ValidationError

from flask import request

class LoginForm(Form):
    """The default login form"""

    username = TextField("Username",
                         validators=[Required(message="Username missing")])
    password = PasswordField("Password",
                             validators=[Required(message="Password not provided")])
    remember = BooleanField("Remember Me", default=True)
    next = HiddenField()
    submit = SubmitField("Login")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.next.data = request.args.get('next', None)

    def validate_username(form, field):
        from models import User
        u1 = User.query.get(field.data)
        if not u1:
            raise ValidationError('User not found')

    def validate_password(form, field):
        from models import User
        u1 = User.query.get(form.username.data)
        if u1:
            if not u1.check_password(field.data):
                raise ValidationError('Password wrong')
