import os
# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Statement for enabling the development environment
DEBUG = True

# Define the database we are working with
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = 'postgres'
DATABASE_PATH = 'localhost:5432/mydb'

SQLALCHEMY_DATABASE_URI = 'postgresql://' + \
    DATABASE_USER + ':' + \
    DATABASE_PASSWORD + '@' + \
    DATABASE_PATH

DATABASE_CONNECT_OPTIONS = {}

# Suppress warning
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for signing the data. 
CSRF_SESSION_KEY = "de43cb1de1d68845beaf5d05"

# Secret key for signing cookies
SECRET_KEY = "c7f703f26e32c0ba4ccd9ab1"