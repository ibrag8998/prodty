from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import g
from flask import session

from prodty.db import get_db
from prodty.helpers import templated, to_index

from .tstamp import recognize


class SQL:
    get_user_tasks = ' \
        SELECT * \
        FROM task \
        INNER JOIN user \
        ON user.id = task.author_id \
        WHERE user.id = ? \
        ORDER BY pub_date DESC'

    add_task = ' \
        INSERT INTO task (author_id, content, tstamp) \
        VALUES (?, ?, ?)'

    delete_task_by_id = '\
        DELETE \
        FROM task \
        WHERE id = ?'

    update_timestamp_by_id = '\
        UPDATE task \
        SET tstamp = ? \
        WHERE id = ?'

    update_content_by_id = '\
        UPDATE task \
        SET content = ? \
        WHERE id = ?'

    get_task_by_id = '\
        SELECT * \
        FROM task \
        WHERE id = ?'

    def row_to_dict(row):
        keys = ['id', 'author_id', 'content', 'pub_date', 'tstamp']
        d = {}
        i = 0
        for v in row:
            d[keys[i]] = v
            i += 1
        return d


def get_tasks():
    return get_db().execute(SQL.get_user_tasks, (g.user['id'],)).fetchall()


def save_last_pop(id_):
    session['last_task_pop'] = SQL.row_to_dict(
        get_db().execute(
            SQL.get_task_by_id, (id_,)
        ).fetchone())


bp = Blueprint('task', __name__)


# functionality of this blueprint only available for
# logged in users. I know, this is not user-friendly,
# but for now I want to focus on developing task blueprint.
# Later, I probably will take care about this ux problem,
# but I'm not sure because I also need to implement tests.
# Hope you understand what I am talking about :D
@bp.before_request
def check_if_logged():
    if g.user is None:
        return redirect(url_for('auth.signin'))


@bp.route('/')
@templated
def index():
    return {'tasks': get_tasks()}


@bp.route('/add', methods=['POST'])
def add():
    task = request.form.get('new-task', '')

    if not task:
        flash('No task typed :( Are you lazy?')
        return to_index()

    tstamp = recognize(task)

    db = get_db()
    db.execute(SQL.add_task, (g.user['id'], task, tstamp))
    db.commit()

    # when the task is added, I want user to stay at
    # that page so he can add more tasks quickly.
    # So I flash message and return needed template
    flash('Added!')
    return to_index()


@bp.route('/edit/<int:id_>', methods=['POST'])
def edit(id_):
    task = request.form.get('task', '')

    if not task:
        # if task user selected the task and deleted its
        # content, this probably means He want to delete it
        return done(id_)

    db = get_db()
    tstamp = recognize(task)

    db.execute(SQL.update_content_by_id, (task, id_))
    db.execute(SQL.update_timestamp_by_id, (tstamp, id_))
    db.commit()
    return to_index()


@bp.route('/done/<int:id_>', methods=['POST'])
def done(id_):
    save_last_pop(id_)

    db = get_db()
    db.execute(SQL.delete_task_by_id, (id_,))
    db.commit()
    flash('Done! Good job! (undo)')
    # 'undo' is unique message, see wrapper.html
    return to_index()


# remove timestamp
@bp.route('/rmts/<int:id_>', methods=['POST'])
def rmts(id_):
    save_last_pop(id_)

    db = get_db()
    # set tstamp to NULL
    db.execute(SQL.update_timestamp_by_id, (None, id_))
    db.commit()
    flash('Removed! (undo)')
    return to_index()


@bp.route('/restore', methods=['POST'])
def restore():
    if 'last_task_pop' not in session:
        flash('No')
        return to_index()

    db = get_db()
    # contains info about last popped before pop
    last = session['last_task_pop'] # just for short
    # contains info about last popped after pop
    task = db.execute(SQL.get_task_by_id, (last['id'],)).fetchone()

    # if last pop was deleting (done), means task is None
    if not task:
        # insert last popped task
        db.execute(SQL.add_task, (
            last['author_id'],
            last['content'],
            last['tstamp']
        ))
    # elif task has no tstamp, means tstamp was deleted
    # so task['tstamp'] is None
    elif not task['tstamp']:
        db.execute(SQL.update_timestamp_by_id, (last['tstamp'], last['id']))
    # for some extraordinary cases huh
    else:
        flash('Nothing to undo')

    db.commit()

    return to_index()

