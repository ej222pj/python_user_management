from flask import jsonify
from datetime import datetime
from flaskr_init import db


class User(db.Model):
    """
    User - This class is the representation of the database model User.
    """
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(50))
    address2 = db.Column(db.String(50))
    city = db.Column(db.String(120))
    zip_code = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    ssn = db.Column(db.String(13))
    expiry_date = db.Column(db.Date)
    create_date = db.Column(db.Date)
    status = db.Column(db.String(50))

    def __init__(self, id=None, firstname=None, lastname=None, email=None, phone=None, address=None, address2=None, city=None,
                 zip_code=None, gender=None, ssn=None, expiry_date=None, create_date=None, status=None):
        """
        Called when creating a new User class.

        :param id: Id of the User
        :type id: integer
        :param firstname: Users firstname
        :type firstname: string
        :param lastname: Users lastname
        :type lastname: string
        :param email: Email to the User
        :type email: string
        :param phone: Users phone number
        :type phone: string
        :param address: Address to the user
        :type address: string
        :param address2: Second Address to the user
        :type address2: string
        :param city: City of the user
        :type city: string
        :param zip_code: Zip Code to the User
        :type zip_code: string
        :param gender: Users gender
        :type gender: string
        :param ssn: Users SSN
        :type ssn: string
        :param expiry_date: Expire date of the users membership
        :type expiry_date: date
        :param create_date: Create date of the user
        :type create_date: date
        :param status: Users status
        :type status: string
        """
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.address = address
        self.address2 = address2
        self.city = city
        self.zip_code = zip_code
        self.gender = gender
        self.ssn = ssn
        self.expiry_date = expiry_date
        self.create_date = create_date
        self.status = status

        if self.create_date is None:
            self.create_date = datetime.now()

    def dict(self):
        return {'id': self.id, 'firstname': self.firstname, 'lastname': self.lastname, 'email': self.email,
                'phone': self.phone, 'address': self.address, 'address2': self.address2, 'city': self.city,
                'zip_code': self.zip_code, 'gender': self.gender, 'ssn': self.ssn, 'expiry_date': str(self.expiry_date),
                'create_date': str(self.create_date), 'status': self.status
                }

    def json(self):
        return jsonify(self.dict())
