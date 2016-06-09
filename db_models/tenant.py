from flask import jsonify
from datetime import datetime
from flaskr_init import db


class Tenant(db.Model):
    """
    Tenant - This class is the representation of the database model Tenant.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    image = db.Column(db.String(200))
    create_date = db.Column(db.Date)
    company_name = db.Column(db.String(100))
    address = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    zip_code = db.Column(db.String(10))
    city = db.Column(db.String(120))
    email = db.Column(db.String(120))

    def __init__(self, username=None, password=None, image=None, create_date=None, company_name=None,
                 address=None, phone=None, zip_code=None, city=None, email=None):
        """
        Called when creating a new Tenant class.

        :param username: Tenants username
        :type username: string (80)
        :param password: Tenants password
        :type password: string (80)
        :param image: Image url
        :type image: string (200)
        :param create_date: Create date of the Tenant
        :type create_date: date
        :param company_name: Company name to the company
        :type company_name: string (100)
        :param address: Address to the company
        :type address: string (50)
        :param phone: Phone to the company or the owner
        :type phone: string  (20)
        :param zip_code: Zip Code to the company
        :type zip_code: string (10)
        :param city: City the company is located in
        :type city: string (120)
        :param email: Email to the company
        :type email: string (120)
        """
        self.username = username
        self.password = password
        self.image = image
        self.create_date = datetime.now()
        self.company_name = company_name
        self.address = address
        self.phone = phone
        self.zip_code = zip_code
        self.city = city
        self.email = email

        # if self.create_date is None:
        # self.create_date = datetime.now()

    def dict(self):
        """
        :return: Dictionary representation of the tenant class.
        :rtype: Dictionary
        """
        return {'id': self.id,
                'username': self.username,
                'password': self.password,
                'image': self.image,
                'create_date': self.create_date,
                'company_name': self.company_name,
                'address': self.address,
                'phone': self.phone,
                'zip_code': self.zip_code,
                'city': self.city,
                'email': self.email
                }

    def json(self):
        return jsonify(self.dict())
