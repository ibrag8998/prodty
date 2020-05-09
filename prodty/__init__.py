import os

from flask import Flask
from flask import render_template

from . import db
from . import auth
from .task import task
from .task.tstamp import tstamp_to_dt


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['DATABASE'] = os.path.join(app.instance_path, 'prodty.sqlite')

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(task.bp)
    # the following line lets us use ``` url_for('index') ```
    # instead of ``` url_for('task.index') ```
    app.add_url_rule('/', endpoint='index')

    app.add_template_filter(tstamp_to_dt, 'todt')

    @app.route('/hello')
    def hello():
        return 'Hello!'

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('page_not_found.html'), 404

    return app
