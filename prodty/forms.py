from wtforms import (
    Form,
    StringField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import (
    Length,
    DataRequired,
    EqualTo,
)


class AuthForm(Form):
    password_validators = [
        Length(6, 25, 'Password must be between 6 and 25 characters length'),
        DataRequired('Password cannot be empty'),
    ]

    username = StringField('Username', [
        Length(4, 25, 'Username must be between 4 and 25 characters length')
    ])
    password = PasswordField('Password', password_validators)
    submit = SubmitField('Sign Up')


class SignUpForm(AuthForm, Form):
    password_validators = AuthForm.password_validators + [
        EqualTo('confirm', 'Passwords must match'),
    ]
    password = PasswordField('Password', password_validators)
    confirm = PasswordField('Repeat password')


class SignInForm(AuthForm, Form):
    pass

