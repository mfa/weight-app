from flask import Flask, Response, request, abort, redirect, flash, url_for
from flask import render_template
from flask.ext.login import LoginManager, UserMixin
from flask.ext.login import login_required, login_user, logout_user , current_user
from flask.ext.sqlalchemy import SQLAlchemy
import os

from forms import LoginForm

app = Flask(__name__)

# config
if os.getenv('DEV') == 'yes':
    app.config.from_object('config.DevelopmentConfig')
    app.logger.info("Config: Development")
elif os.getenv('TEST') == 'yes':
    app.config.from_object('config.TestConfig')
    app.logger.info("Config: Test")
else:
    app.config.from_object('config.ProductionConfig')
    app.logger.info("Config: Production")

db = SQLAlchemy(app)

# flask-login
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "login"

@app.route('/')
@login_required
def index():
    if current_user._user:
        user = current_user._user
    else:
        user = False
    return render_template('index.html',
                           user=user)

@login_manager.user_loader
def load_user(user):
    from models import User
    u1 = User.query.get(user)
    if u1:
        return DbUser(user)
    else:
        return None

# User class
class DbUser(object):
    """Wraps User object for Flask-Login"""
    def __init__(self, user):
        self._user = user

    def get_id(self):
        return unicode(self._user)

    def is_active(self):
        # FIXME
        #        return self._user.enabled
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True 

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

        from models import User
        u1 = User.query.get(username)
        if login_user(DbUser(u1.username)):
            flash("You have logged in")
            next = request.args.get('next')
            return redirect(next or url_for('index'))

    return render_template('login.html',
                           form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have logged out')
    return(redirect(url_for('login')))

