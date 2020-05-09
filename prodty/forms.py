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
    username = StringField('Username', [Length(4, 25)])
    password = PasswordField('Password', [
        Length(6, 25),
        DataRequired(),
    ])
    submit = SubmitField('Sign Up')


class SignUpForm(AuthForm, Form):
    password = PasswordField('Password', [
        Length(6, 25),
        DataRequired(),
        EqualTo('confirm', 'Passwords must match'),
    ])
    confirm = PasswordField('Repeat password')


class SignInForm(AuthForm, Form):
    pass

