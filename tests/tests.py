import os
import unittest
import grequests
import sys
import tempfile
from config import SQLALCHEMY_DATABASE_URI
import flaskr
# sys.path.append('../')


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config[SQLALCHEMY_DATABASE_URI] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config[SQLALCHEMY_DATABASE_URI])


if __name__ == '__main__':
    unittest.main()