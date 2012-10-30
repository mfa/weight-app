""" Part of weight_app

    :copyright: (c) 2012 by Andreas Madsack.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask, render_template
from flask.ext.login import LoginManager, UserMixin
from flask.ext.login import current_user
from flask.ext.sqlalchemy import SQLAlchemy
import os
import datetime

db = SQLAlchemy()

def create_app():
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

    db.init_app(app)

    ## register views
    from views import weight_pages
    app.register_blueprint(weight_pages)

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

    app.register_error_handler(401, error401)
    app.register_error_handler(404, error404)
    app.register_error_handler(500, error500)

    app.jinja_env.filters['year'] = format_year

    # flask-login
    login_manager = LoginManager()
    login_manager.setup_app(app)
    login_manager.login_view = ".login"
    
    @login_manager.user_loader
    def load_user(user):
        from models import User
        u1 = User.query.get(user)
        if u1:
            return DbUser(user)
        else:
            return None

    return app


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

# errorhandlers
def error401(e):
    return render_template('error.html',
                           errorcode=401), 401

def error404(e):
    return render_template('error.html',
                           errorcode=404), 404

def error500(e):
    return render_template('error.html',
                           errorcode=500), 500

# filters
def format_year(value, format='%Y'):
    return value.strftime(format)
