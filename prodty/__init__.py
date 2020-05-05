import os

from flask import Flask

from . import db
from . import auth


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['DATABASE'] = os.path.join(
        app.instance_path, 'prodty.sqlite')

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    app.register_blueprint(auth.bp)

    @app.route('/hello')
    def hello():
        return 'Hello!'

    return app

