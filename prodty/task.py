from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import g

from .db import get_db
from .auth import login_required
from . import sqls


bp = Blueprint('task', __name__)


def get_tasks():
    return get_db().execute(sqls.get_user_tasks, (g.user['id'],)).fetchall()


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
def index():
    return render_template('task/index.html', tasks=get_tasks())


@bp.route('/add', methods=['GET', 'POST'])
def add():
    template = 'task/add.html'
    if request.method == 'POST':
        task = request.form.get('task', '')

        # it will be bloat if I will use validations.validate
        # func here because I just need to check one input
        # if it is plain
        if not task:
            return render_template(template, tasks=get_tasks())

        db = get_db()
        db.execute(sqls.add_task, (g.user['id'], task))
        db.commit()

        # when the task is added, I want user to stay at
        # that page so he can add more tasks quickly.
        # So I flash message and return needed template
        flash('Added!')

    return render_template(template, tasks=get_tasks())


@bp.route('/done/<int:id_>', methods=['POST'])
def done(id_):
    db = get_db()
    db.execute(sqls.delete_task_by_id, (id_,))
    db.commit()
    return redirect(url_for('index'))

