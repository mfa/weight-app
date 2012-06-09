#from flask import Flask, Response, request, abort, redirect, flash, url_for
from flask import Flask, render_template
from flask.ext.login import LoginManager, UserMixin
from flask.ext.login import current_user
from flask.ext.sqlalchemy import SQLAlchemy
import os
import datetime

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


@app.context_processor
def context_processor():
    """Add variables to context
    """
    if hasattr(current_user, '_user'):
        curuser = current_user._user
    else:
        # if user is not logged in
        curuser = ""

    return {'today': datetime.date.today,
            'user':curuser,
            }


## register views
from views import weight_pages
app.register_blueprint(weight_pages)


# errorhandlers
@app.errorhandler(401)
def error401(e):
    return render_template('error.html',
                           errorcode=401), 401

@app.errorhandler(404)
def error404(e):
    return render_template('error.html',
                           errorcode=404), 404

@app.errorhandler(500)
def error500(e):
    return render_template('error.html',
                           errorcode=500), 500

# filters
def format_year(value, format='%Y'):
    return value.strftime(format)

app.jinja_env.filters['year'] = format_year
