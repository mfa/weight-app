from flask import Flask, Response, request, abort, redirect, flash, url_for
from flask import render_template
from flask.ext.login import LoginManager, UserMixin
from flask.ext.login import login_required, login_user, logout_user , current_user
from flask.ext.sqlalchemy import SQLAlchemy
import os

from forms import LoginForm, ProfileForm

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
    import datetime
    d = {'today': datetime.date.today, 
         'user':current_user._user
         }
    return d


## views

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

        from models import User
        u1 = User.query.get(username)
        if login_user(DbUser(u1.username)):
            flash("You have logged in", "info")
            next = request.args.get('next')
            return redirect(next or url_for('index'))

    return render_template('login.html',
                           form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have logged out', "info")
    return(redirect(url_for('login')))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    from models import User
    u1 = User.query.get(current_user._user)
    form = ProfileForm(obj=u1)

    if form.validate_on_submit():

        if 'firstname' in request.form:
            u1.firstname = request.form['firstname']

        if 'lastname' in request.form:
            u1.lastname = request.form['lastname']

        if 'email' in request.form:
            u1.email = request.form['email']

        if 'password' in request.form:
            u1.set_password(request.form['password'])

        # TODO: set default scale

        db.session.add(u1)
        db.session.commit()
        flash('Data saved', 'info')

    return render_template('profile.html',
                           form=form)

@login_required
@app.route("/weight/")
@app.route("/weight/<wid>/", methods=["GET","POST"])
def weight(wid=None):
    from models import Weight

    if wid:
        # edit weight
        elem = Weight.query.get(wid)

        # is this weight from logged_in user? or is user admin?
        if elem.user_username == current_user._user or \
                current_user._user == 'admin':
            return Response(str(elem))
        else:
            # unauthorized
            abort(401)
    else:
        # show table of weights
        page = request.args.get('page', '')
        if page.isdigit():
            page = int(page)
        else:
            page = 1

        elements = Weight.query.order_by('wdate desc').filter_by(
            user_username=unicode(current_user._user)).paginate(
            page, per_page=10)
        
        return render_template('weight_list.html',
                               elements=elements.items,
                               paginate=elements)

