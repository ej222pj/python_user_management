# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='Python User Management',
    version='1.0.0',
    description='User Management with focus on learning Python',
    long_description=(read('README.md') + '\n\n' +
                      read('HISTORY.rst') + '\n\n' +
                      read('AUTHORS.rst')),
    url='https://github.com/ej222pj/python_user_management',
    license='MIT',
    author='Eric Sjöström Jennerstrand',
    author_email='eric.sj11@hotmail.se',
    py_modules=['python_user_management'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['Flask', 'Flask-WTF', 'Flask-SQLAlchemy' , 'Jinja2', 'WTForms',
                      'Werkzeug', 'grequests', 'pyfiglet', 'py-bcrypt']
)
