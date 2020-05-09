from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from flask import g
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from .db import get_db
from .helpers import templated
from .helpers import to_index
from .forms import SignUpForm, SignInForm


class SQL:
    add_user = '\
        INSERT INTO user (username, password) \
        VALUES (?, ?)'

    get_user_by_username = '\
        SELECT * \
        FROM user \
        WHERE username = ?'


def valid_post(form):
    """
    Yes, there is form.validate_on_submit() to use
    with FlaskForm instances, but for some reasons there
    is a bug with it: form.errors is empty, but
    form.validate() is False.
    So here is my skill of problem solving XD
    """
    return request.method == 'POST' and form.validate()


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=['GET', 'POST'])
@templated
def signup():
    form = SignUpForm(request.form)
    if valid_post(form):
        username = form.username.data
        password = form.password.data

        db = get_db()

        user = db.execute(SQL.get_user_by_username, (username, )).fetchone()
        if user:
            flash('Such username already taken')
            return {'form': form}

        db.execute(SQL.add_user, (username, generate_password_hash(password)))
        db.commit()

        # Sometimes when you sign up on the site, you may forget password.
        # So here prodty redirects user to signin view where he will type
        # his credentials again and minimize chance of forgetting something.
        return redirect(url_for('auth.signin'))

    return {'form': form}


@bp.route('/signin', methods=['GET', 'POST'])
@templated
def signin():
    form = SignInForm(request.form)
    if valid_post(form):
        username = form.username.data
        password = form.password.data

        db = get_db()
        user = db.execute(SQL.get_user_by_username, (username, )).fetchone()

        if not user:
            flash('No such user')
            return {'form': form}

        if not check_password_hash(user['password'], password):
            flash('Incorrect password')
            return {'form': form}

        # add username to session, so site will think user is logged in
        # (see load_user() func)
        session.clear()
        session['username'] = user['username']

        # successful login, redirect to main page
        return to_index()

    return {'form': form}


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
                                  (username, )).fetchone()
