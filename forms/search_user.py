from flask.ext.wtf import Form
from wtforms import StringField


class SearchUser(Form):
    """
    A representation of the form for searching a user.

    :param firstname: Firstname of the user.
    :type firstname: string (80)
    :param lastname: Lastname of the user.
    :type lastname: string (80)
    :param city: City of the user.
    :type city: string (120)
    :param email: Email address of the user.
    :type email: string (120)
    """

    firstname = StringField('firstname', validators=[])
    lastname = StringField('lastname', validators=[])
    city = StringField('city', validators=[])
    email = StringField('email', validators=[])
