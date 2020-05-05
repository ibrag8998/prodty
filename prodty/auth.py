from functools import wraps

from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import g

from werkzeug.security import generate_password_hash

from .db import get_db
from .validations import validate
from . import sqls


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    template = 'auth/signup.html'
    if request.method == 'POST':
        # get data
        username = request.form['username']
        passwd = request.form['password']
        passwd2 = request.form['password2']

        db = get_db()
        user = db.execute(sqls.get_user_by_username, (username,)).fetchone()

        if not validate(username, passwd, passwd2, user, rule='signup'):
            return render_template(template)

        # on errors detected, add user
        db.execute(sqls.add_user, (username, generate_password_hash(passwd)))
        db.commit()

        # Sometimes when you sign up on the site, you may forget password.
        # So here prodty redirects user to signin view where he will type
        # his credentials again and minimize chance of forgetting something.
        return redirect(url_for('auth.signin'))

    return render_template(template)


@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    template = 'auth/signin.html'
    if request.method == 'POST':
        # get data
        username = request.form['username']
        passwd = request.form['password']

        db = get_db()
        user = db.execute(sqls.get_user_by_username, (username,)).fetchone()

        if not validate(username, passwd, user, rule='signin'):
            return render_template(template)

        # add username to session, so site will think user is logged in
        # (see load_user() func)
        session.clear()
        session['username'] = user['username']

        # note: this is just for testing. Of course, its bad practice to
        # redirect user to signup after signin, but I have not implemented
        # other views yet, so temporary, this redirect will be here :D
        return redirect(url_for('auth.signup'))

    return render_template(template)


@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('auth.signin'))


@bp.before_app_request
def load_user():
    username = session.get('username')
    if username is None:
        g.user = None
    else:
        g.user = get_db().execute(sqls.get_user_by_username,
                                  (username,)).fetchone()


def login_requried(view):
    @wraps(view)
    def wrapper_view(*args, **kwargs):
        if g.user is None:
            # user is not logged in, so he will be redirected to signin view
            return redirect(url_for('auth.signin'))

        # user is logged in, so he will get requested view
        return view(*args, **kwargs)

    return wrapper_view
