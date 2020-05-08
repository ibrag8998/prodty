from functools import wraps

from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    g
)
from werkzeug.security import generate_password_hash

from .db import get_db
from .helpers import templated, to_index
from .forms import SignUpForm
from .validations import validate


class SQL:
    add_user = '\
        INSERT INTO user (username, password) \
        VALUES (?, ?)'

    get_user_by_username = '\
        SELECT * \
        FROM user \
        WHERE username = ?'


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=['GET', 'POST'])
@templated()
def signup():
    form = SignUpForm(request.form)
    flash(form.errors)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        db = get_db()

        user = db.execute(SQL.get_user_by_username, (username,)).fetchone()
        if user:
            return dict(form=form)

        db.execute(SQL.add_user, (username, generate_password_hash(password)))
        db.commit()

        # Sometimes when you sign up on the site, you may forget password.
        # So here prodty redirects user to signin view where he will type
        # his credentials again and minimize chance of forgetting something.
        return redirect(url_for('auth.signin'))

    flash(form.errors)
    return dict(form=form)


@bp.route('/signin', methods=['GET', 'POST'])
@templated()
def signin():
    if request.method == 'POST':
        # get data
        username = request.form.get('username', '')
        passwd = request.form.get('password', '')

        db = get_db()
        user = db.execute(SQL.get_user_by_username, (username,)).fetchone()

        if not validate(username, passwd, user, rule='signin'):
            return {}

        # add username to session, so site will think user is logged in
        # (see load_user() func)
        session.clear()
        session['username'] = user['username']

        # successful login, redirect to main page
        return to_index()

    return {}


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
        g.user = get_db().execute(SQL.get_user_by_username,
                                  (username,)).fetchone()

