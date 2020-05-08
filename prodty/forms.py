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


class SignUpForm(Form):
    username = StringField('Username', [Length(4, 25)])
    password = PasswordField('Password', [
        Length(6, 25),
        DataRequired(),
        EqualTo('confirm', 'Passwords must match'),
    ])
    confirm = PasswordField('Repeat password')
    submit = SubmitField('Sign Up')

