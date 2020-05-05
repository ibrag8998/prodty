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


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    template = 'auth/signup.html'
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
        passwd2 = request.form['password2']

        if not validate(username, passwd, passwd2, rule='signup'):
            return render_template(template)

        db.execute('INSERT INTO user (username, password)'
                   ' VALUES (?, ?)',
                   (username, generate_password_hash(passwd)))
        db.commit()

        return redirect(url_for('auth.signin'))

    return render_template(template)


@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    template = 'auth/signin.html'
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']

        db = get_db()
        user = db.execute('SELECT * FROM user WHERE username=?',
                          (username,)).fetchone()

        if not validate(username, passwd, user, rule='signin'):
            return render_template(template)

        session.clear()
        session['user_id'] = user['id']

        return redirect(url_for('auth.signup'))

    return render_template(template)


@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('auth.signin'))


@bp.before_app_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id=?',
                                  (user_id,)).fetchone()

