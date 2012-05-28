from flask.ext.wtf import Form, TextField, PasswordField, SubmitField, \
     HiddenField, Required, BooleanField

class LoginForm(Form):
    """The default login form"""

    email = TextField("Email Address",
        validators=[Required(message="Email not provided")])
    password = PasswordField("Password",
        validators=[Required(message="Password not provided")])
    remember = BooleanField("Remember Me")
    next = HiddenField()
    submit = SubmitField("Login")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.next.data = request.args.get('next', None)
