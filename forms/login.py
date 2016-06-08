from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, validators


class Login(Form):
    """
    A representation of the form for login.

    :param username: Username of a tenant.
    :type username: string (80)
    :param password: Password of a tenant.
    :type password: string (80)
    """
    username = StringField('username', [validators.Length(max=80,
                                                          message='Username is to long, 80 characters is maximum'),
                                        validators.DataRequired(message='Username is required')])

    password = PasswordField('password', [validators.Length(max=80,
                                                            message='Password is to long, 80 characters is maximum'),
                                          validators.DataRequired(message='Password is required')])