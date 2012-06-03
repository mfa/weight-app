from flask import Flask, Response, request, abort, redirect, flash, url_for
from flask import render_template
from flask.ext.login import LoginManager, UserMixin
from flask.ext.login import login_required, login_user, logout_user , current_user
from flask.ext.sqlalchemy import SQLAlchemy
import os
import datetime

from forms import LoginForm, ProfileForm, WeightForm, ScaleForm

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


## views

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

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
    from models import User, Scale
    u1 = User.query.get(current_user._user)
    form = ProfileForm(obj=u1)

    form.default_scale.choices = [(g.name, g.name) 
                                  for g in Scale.query.order_by('name')]
    form.default_scale.choices.insert(0, ("", "Select..."))

    if form.validate_on_submit():

        if 'firstname' in request.form:
            u1.firstname = request.form['firstname']

        if 'lastname' in request.form:
            u1.lastname = request.form['lastname']

        if 'email' in request.form:
            u1.email = request.form['email']

        if 'password' in request.form:
            u1.set_password(request.form['password'])

        if 'default_scale' in request.form:
            u1.default_scale_name = request.form['default_scale']

        db.session.add(u1)
        db.session.commit()
        flash('Data saved', 'info')

    if u1.default_scale_name:
        form.default_scale.data = u1.default_scale_name


    return render_template('profile.html',
                           form=form)

@app.route("/weight/")
@app.route("/weight/<wid>/", methods=["GET","POST"])
@login_required
def weight(wid=None):
    from models import Weight, Scale, User
    import math

    if not wid and 'wid' in request.args:
        wid = request.args.get('wid')

    if wid:
        # edit weight
        elem = Weight.query.get(wid)

        # get min/max for buttons
        x = Weight.query.order_by(Weight.wdate).limit(20).all()
        if x:
            wmin = int(math.floor(min([i.weight for i in x])) - 1)
            wmax = int(math.ceil(max([i.weight for i in x])) + 2)
        else:
            wmin=70
            wmax=75

        if elem:
            # is this weight from logged_in user? or is user admin?
            if elem.user_username == current_user._user or \
                    current_user._user == 'admin':

                form = WeightForm(obj=elem)
            else:
                # unauthorized
                abort(401)
        else:
            # add
            form = WeightForm()

        # get scales list
        form.scale_name.choices = [(g.name, g.name) 
                                   for g in Scale.query.order_by('name')]
        form.scale_name.choices.insert(0, ("", "Select..."))

        if form.validate_on_submit():
            if not elem:
                elem = Weight(weight=request.form['weight'])

            if 'weight' in request.form:
                elem.weight = request.form['weight']

            if 'wdate' in request.form:
                elem.wdate = datetime.datetime.strptime(request.form['wdate'],
                                                        '%Y-%m-%d')

            if 'scale_name' in request.form:
                elem.scale_name = request.form['scale_name']

            elem.user_username = current_user._user

            db.session.add(elem)
            db.session.commit()
            flash('Data saved', 'info')

        if elem:
            if elem.scale_name:
                form.scale_name.data = elem.scale_name
        else:
            u1 = User.query.get(current_user._user)
            if u1.default_scale_name:
                form.scale_name.data = u1.default_scale_name

        return render_template('weight_edit.html',
                               form=form,
                               wrange=range(wmin,wmax),)
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
                               paginate=elements,
                               show_comment=False,)

@app.route("/scale/")
@app.route("/scale/<sid>/", methods=["GET","POST"])
@login_required
def scale(sid=None):
    from models import Scale

    if not sid and 'sid' in request.args:
        sid = request.args.get('sid')

    if sid:
        # edit weight
        elem = Scale.query.get(sid)

        if elem:
            form = ScaleForm(obj=elem)
        else:
            # add
            form = ScaleForm()

        if form.validate_on_submit():
            if not elem:
                elem = Scale(name=request.form['name'])

            if 'name' in request.form:
                elem.name = request.form['name']

            if 'owner' in request.form:
                elem.owner = request.form['owner']

            if 'model' in request.form:
                elem.model = request.form['model']

            if 'comment' in request.form:
                elem.comment = request.form['comment']

            db.session.add(elem)
            db.session.commit()
            flash('Data saved', 'info')

        return render_template('scale_edit.html',
                               form=form,)
    else:
        # show table of weights
        page = request.args.get('page', '')
        if page.isdigit():
            page = int(page)
        else:
            page = 1

        elements = Scale.query.order_by('name').paginate(
            page, per_page=10)
        
        return render_template('scale_list.html',
                               elements=elements.items,
                               paginate=elements,)

# TODO: errorpages (401, 404, 500)

# filters
def format_year(value, format='%Y'):
    return value.strftime(format)

app.jinja_env.filters['year'] = format_year
