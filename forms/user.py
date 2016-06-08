from flask.ext.wtf import Form
from wtforms import StringField, RadioField, DateField, validators


class User(Form):
    """
    A representation of the form for editing a user.

    :param firstname: Firstname of the user.
    :type firstname: string (80)
    :param lastname: Lastname of the user.
    :type lastname: string (80)
    :param email: Email address of the user.
    :type email: string (120)
    :param phone: Phone number of the user.
    :type phone: string (20)
    :param address: Address 1 of the user.
    :type address: string (50)
    :param address2: Address 2 of the user.
    :type address2: string (50)
    :param city: City of the user.
    :type city: string (120)
    :param zip_code: Zip code of the city.
    :type zip_code: string (10)
    :param gender: Gender of the user.
    :type gender: string (10)
    :param ssn: Social Security Number.
    :type ssn: string (13)
    :param expiry_date: Expire date of the users membership.
    :type expiry_date: date
    :param status: Status of the users membership.
    :type status: string (50)
    """
    firstname = StringField('firstname', [validators.Length(max=80,
                                                            message='Firstname to long, 25 characters is maximum'),
                                          validators.DataRequired(message='Firstname is required')])

    lastname = StringField('lastname', [validators.Length(max=80,
                                                          message='Lastname to long, 30 characters is maximum'),
                                        validators.DataRequired(message='Lastname is required')])

    email = StringField('email', [validators.Length(max=120,
                                                    message='Email to long, 120 characters is maximum'),
                                  validators.Email(message='Email is not in valid format')])

    phone = StringField('phone', [validators.Length(max=20,
                                                    message='Phone number to long, 20 characters is maximum'),
                                  validators.DataRequired(message='Phone number is required')])

    address = StringField('address', [validators.Length(max=50,
                                                        message='Address to long, 50 characters is maximum'),
                                      validators.DataRequired(message='Address is required')])

    address2 = StringField('address2', [validators.Length(max=50,
                                                          message='Second address to long, 50 characters is maximum')])

    city = StringField('city', [validators.Length(max=120,
                                                  message='City to long, 120 characters is maximum'),
                                validators.DataRequired(message='City is required')])

    zip_code = StringField('zip_code', [validators.Length(max=10,
                                                          message='Zip code is to long, 20 characters is maximum'),
                                        validators.DataRequired(message='Zip code is required')])

    gender = RadioField('gender', [validators.DataRequired(message='Gender is required')],
                        choices=[('male', 'male'), ('female', 'female'), ('other', 'other')])

    ssn = StringField('ssn', [validators.Length(max=13, message='SSN to long, 14 characters is maximum')])

    expiry_date = DateField('expiry_date', [validators.Optional()], format='%Y-%m-%d', description="DESC1")

    status = RadioField('status', [validators.DataRequired(message='Status is required')],
                        choices=[('Active', 'active'), ('Inactive', 'inactive'), ('Frozen', 'frozen'),
                                 ('Free', 'free'), ('Special', 'special')])
