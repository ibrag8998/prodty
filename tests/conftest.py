import os
import tempfile

import pytest
from prodty import create_app
from prodty.db import get_db, init_db

import sqls


class AuthActions:
    def __init__(self, client):
        self.client = client

    def login(self, username='test_bot1', password='tester1'):
        return self.client.post('/auth/signin', data={
            'username': username,
            'password': password
        })

    def logout(self):
        return self.client.post('/auth/logout')


# to use auth.login() or auth.logout()
@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SECRET_KEY': 'testing'
    }) # test_config is passed

    with app.app_context():
        init_db()
        db = get_db()
        db.execute(sqls.add_users)
        db.execute(sqls.add_tasks)
        db.commit()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


# to test requests without flask server active and with
# convenient urls building
@pytest.fixture
def client(app):
    return app.test_client()


# to test cli command
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

