import sqlite3

import pytest
from prodty.db import get_db


def test_get_close_db(app):
    # test if db is the same in one app_context
    with app.app_context():
        db = get_db()
        assert db is get_db()

    # test if db is closed, because db should close after
    # each request. request ends in with statement above
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    # error message contains 'closed' word
    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    # monkey patch is pytest's default fixture
    class Recorder:
        called = False

    def fake_init_db():
        Recorder.called = True

    # instead of real init_db() We want to call fake_init_db()
    # because We just testing if init-db command calls init_db()
    monkeypatch.setattr('prodty.db.init_db', fake_init_db)
    # run command
    result = runner.invoke(args=['init-db'])
    # if init-db command successfully done its job, message
    # will be shown, and it contains 'Initialized' word in it
    assert 'Initialized' in result.output
    assert Recorder.called

