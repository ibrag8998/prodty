import pytest
from flask import g, session
from prodty.db import get_db

import sqls


# valid input
def test_signup(client, app):
    # basic
    assert client.get('/auth/signup').status_code == 200

    # make correct signup request
    resp = client.post('/auth/signup', data={
       'username': 'somelogin',
        'password': '6letter',
        'password2': '6letter'
    })
    # test redirect
    assert resp.headers.get('Location') == 'http://localhost/auth/signin'

    # test if such user now exists
    with app.app_context():
        assert get_db().execute(
            sqls.get_user_by_username, ('somelogin',)
        ).fetchone() is not None


# invalid input
# 6 variants
@pytest.mark.parametrize(
    ('username', 'passwd', 'passwd2', 'message'), (
        ('', '', 'a', b'Username is required'),
        ('a', '', 'a', b'Password is required'),
        ('a', 'a', '', b'Password confirmation is required'),
        ('a', 'a', 'a', b'Password must contain at least 6 characters'),
        ('a', 'abcdef', 'abcdee', b'Passwords does not match'),
        ('test_bot1', 'tester1', 'tester1',
         b'Such username is already taken')
    ))
def test_signup_validation(client, username, passwd, passwd2, message):
    resp = client.post('/auth/signup', data={
        'username': username, 'password': passwd, 'password2': passwd2
    })
    assert message in resp.data


# valid input
def test_login(client, auth):
    # basic
    assert client.get('auth/signin').status_code == 200

    # on success, redirect should happen
    resp = auth.login()
    assert resp.headers.get('Location') == 'http://localhost/'

    # using client in with statement allows accessing session.
    # without it, error should be raised
    with client:
        client.get('/')
        assert session['username'] == 'test_bot1'
        assert g.user['username'] == 'test_bot1'


# invalid input
# 5 variants
@pytest.mark.parametrize(
    ('username', 'passwd', 'message'), (
        ('', '', b'Username is required'),
        ('a', '', b'Password is required'),
        ('a', 'a', b'Password must contain at least 6 characters'),
        ('a', 'abcdef', b'No such user'),
        ('test_bot1', 'incorrect', b'Incorrect password')
    ))
def test_signin_validation(client, username, passwd, message):
    resp = client.post('/auth/signin', data={
        'username': username, 'password': passwd
    })
    assert message in resp.data


# logout is opposite of login
def test_logout(client, auth):
    auth.login()

    with client:
        client.post('/auth/logout')
        assert 'username' not in session

