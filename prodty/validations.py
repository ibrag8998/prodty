from flask import flash
from werkzeug.security import check_password_hash


def validate(*args, rule=None, **kwargs):
    """
    Works like a router and skeleton.

    Calls needed func, for example, if :rule: == 'signin',
    this func calls :validate_signin:. Look at global variable rules.

    If specified validation func raises an AssertionError,
    this func flashes message that is specified in those validators,
    for example, 'Username is required', and returns False.

    Else, when specified validator raises no AssertionError-s,
    this function returns True.

    In views, you simply type:
    ``` if not validate(username, passwd, rule='signin'): ```
    ```     return render_template(template) ```
    Error messages already flashed, so you can just return template,
    it will come with error messages included.
    """

    # check if specified rule is correct.
    # This assert is not in try block, because if it was there,
    # :validate: func will return False when rule not in rules.
    # It means the data is not valid, so error will be flashed and
    # template returned, with this debugging message in it,
    # but you most probably don't want user to see this message.
    assert rule in rules, 'Correct :rule: parameter needed'

    try:
        # call needed func by specified rule and pass all args
        rules[rule](*args, **kwargs)
        return True
    except AssertionError as e:
        flash(str(e))
        return False


def check_plain(*pairs, suffix='is required'):
    """
    This func just checks if input is plain.

    As :pairs:, it takes 2-ible like:
    (input_item, message_if_it_is_plain)

    if :input_item: is plain, you will get AssertionError with message
    like :message_if_it_is_plain: + :suffix:, where suffix by default is
    'is required'. You can change it or make it plain (''), so no suffix will
    appear.
    """
    for item, message in pairs:
        assert item, (message + ' ' + suffix).strip()


def check_passwd_len(passwd, message=None):
    """ Password len needs to be at least 6 characters """
    if message is None:
        message = 'Password must contain at least 6 characters'
    assert len(passwd) >= 6, message


def validate_signup(username, passwd, passwd2, user):
    """ Validation rule for signup """
    # check if username and password are filled in
    check_plain(
        (username, 'Username'),
        (passwd, 'Password'),
        (passwd2, 'Password confirmation')
    )

    # check if passwd len is minimum 6 symbols
    check_passwd_len(passwd)

    # check if passwords match
    assert passwd == passwd2, 'Passwords does not match'

    # check if such username is taken
    assert user is None, 'Such username is already taken'


def validate_signin(username, passwd, user):
    """ Validation rule for signin """
    # check if username or passwd are plain
    check_plain((username, 'Username'), (passwd, 'Password'))

    # check if passwd len is minimum 6 symbols
    check_passwd_len(passwd)

    # check if such user exists
    assert user, 'No such user'

    # check if password hashes match
    assert check_password_hash(user['password'], passwd), \
           'Incorrect password'


rules = {
    'check_plain': check_plain,
    'signup': validate_signup,
    'signin': validate_signin,
}

