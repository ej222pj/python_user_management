from flask.ext.wtf import Form
from wtforms import StringField, validators, PasswordField


class EditTenant(Form):
    """
    A representation of the form for updating a tenants info.

    :param password: Tenants old pass
    :type password: string (80)
    :param new_password: Tenants new pass
    :type new_password: string (80)
    :param repeat_new_password: tenants new pass again
    :type repeat_new_password: string (80)
    :param image: Gym image
    :type image: string (200)
    """
    password = PasswordField('password',
                             [validators.Length(max=80, message='Actual password to long, 80 characters is maximum'),
                              validators.DataRequired(message='Actual password is required to save changes')])

    new_password = PasswordField('new_password',
                                 [validators.Length(max=80,
                                                    message='New password is to long, 80 characters is maximum'),
                                  validators.EqualTo('repeat_new_password', message='New passwords must match')])

    repeat_new_password = \
        PasswordField('repeat_new_password',
                      [validators.Length(max=80, message='New repeated password is to long, 80 characters is maximum')])

    image = StringField('image', [validators.Length(max=200, message='Image URL is to long, can\'t be over 200')])
