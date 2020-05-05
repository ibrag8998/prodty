from flask import flash
from werkzeug.security import check_password_hash

from .db import get_db


def validate(*args, rule=None):
    """
    Works like a router and skeleton.

    Calls needed function, for example, if :rule: == 'signin',
    this function calls :validate_signin:. Why? Look at
    global variable rules.

    If specified validation function raises an AssertionError,
    this function flashes message that is specified in those validators,
    for example, 'Username is required', and returns False.

    Else, when specified validator raised no AssertionError's,
    this function returns True.

    In views, you simply type:
    ``` if not validate(username, passwd, rule='signin'): ```
    ```     return render_template(template) ```
    Error messages alread flashed, so you can just return template,
    it will come with error messages
    """

    # check if specified rule is correct
    # this assert is not in try block, because
    # if it was there, this func will return False,
    # which just means that the data is not valid,
    # then error will be flashed and template returned,
    # but you most probably don't want user to see this message.
    assert rule in rules, 'Correct :rule: parameter needed'

    try:
        # call needed function by specified rule and pass all args
        rules[rule](*args)
        return True
    except AssertionError as e:
        flash(e)
        return False


def check_plain(*pairs, suffix='is required'):
    """
    This func just checks if input is plain.

    As :pairs:, it takes 2-ible like:
    (input_item, message_if_it_is_plain)

    if :input_item: is plain, you will get AssertionError with message
    like :message_if_it_is_plain: + :suffix:, where suffix by default is
    'is required'. You can change or make it plain (''), so no suffix will
    appear.
    """
    for item, message in pairs:
        assert item, (message + ' ' + suffix).strip()


def validate_signup(username, passwd, passwd2):
    """ Validation rule for signup """
    # check if username and password are filled in
    check_plain((username, 'Username'), (passwd, 'Password'))

    # check if passwords match
    assert passwd == passwd2, 'Passwords does not match'

    db = get_db()

    # check if such username is taken
    assert db.execute(
        'SELECT id FROM user WHERE username = ?',
        (username,)
    ).fetchone() is None, 'Such username is already taken'


def validate_signin(username, passwd, user):
    """ Validation rule for signin """
    # check if username or passwd are plain
    check_plain((username, 'Username'), (passwd, 'Password'))

    # check if such user exists
    assert user, 'No such user'

    # check if password hashes match
    assert check_password_hash(user['password'], passwd), \
           'Incorrect password'


rules = {
    'signup': validate_signup,
    'signin': validate_signin,
}

