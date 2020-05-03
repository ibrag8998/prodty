import os

from flask import (
    Flask
)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.route('/hello')
    def hello():
        return 'Hello!'

    return app

