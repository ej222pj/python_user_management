from flask.ext.wtf import Form
from wtforms import StringField, RadioField, PasswordField, validators


class Register(Form):
    """
    A representation of the form for creating a new Tenant.

    :param username: Username of the tenant
    :type username: string (80)
    :param password: Tenants old pass
    :type password: string (80)
    :param repeat_password: tenants new pass again
    :type repeat_password: string (80)
    :param company_name: Tenants Company Name
    :type company_name: string (100)
    :param address: Tenants Address
    :type address: string (50)
    :param phone: Tenants Phone
    :type phone: string (20)
    :param zip_code: Tenants Zip
    :type zip_code: string (10)
    :param city: Tenants City
    :type city: string (120)
    :param email: Tenants Email
    :type email: string (120)
    """
    username = StringField('username', [validators.Length(max=80,
                                                          message='Username is to long, 80 characters is maximum'),
                                        validators.DataRequired(message='Username is required')])

    password = PasswordField('password', [validators.Length(max=80,
                                                            message='Password is to long, 80 characters is maximum'),
                                          validators.DataRequired(message='Password is required'),
                                          validators.EqualTo('repeat_password', message='Passwords doesn\'t match')])

    repeat_password = \
        PasswordField('repeat_password',
                      [validators.Length(max=80, message='Repeated password is to long, 80 characters is maximum'),
                       validators.DataRequired(message='Repeated password is required')])

    company_name = StringField('company_name',
                               [validators.Length(max=100,
                                                  message='Company name is to long, 100 characters is maximum'),
                                validators.DataRequired(message='Company name is required')])

    address = StringField('address', [validators.Length(max=50, message='Address is to long, 50 characters is maximum'),
                                      validators.DataRequired(message='Address is required')])

    phone = StringField('phone', [validators.Length(max=20,
                                                    message='Phone number is to long, 20 characters is maximum'),
                                  validators.DataRequired(message='Phone number is required')])

    zip_code = StringField('zip_code', [validators.Length(max=10,
                                                          message='Zip code is to long, 10 characters is maximum'),
                                        validators.DataRequired(message='Zip code is required')])

    city = StringField('city', [validators.Length(max=50, message='City is to long, 50 characters is maximum'),
                                validators.DataRequired(message='City is required')])

    email = StringField('email', [validators.Length(max=50, message='Email is to long, 50 characters is maximum'),
                                  validators.Email(message='Email is not in valid format'),
                                  validators.DataRequired(message='Email is required')])