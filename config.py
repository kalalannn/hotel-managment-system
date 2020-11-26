import os
# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Statement for enabling the development environment
DEBUG = True

# Define the database we are working with
DATABASE_USER = 'zaczeshwpfbuxb'
DATABASE_PASSWORD = '55fe00bdf6948369b6e9c6171bfb7fac645ac7565fb7189cff441066a08c8963'

SQLALCHEMY_DATABASE_URI = 'postgres://zaczeshwpfbuxb:55fe00bdf6948369b6e9c6171bfb7fac645ac7565fb7189cff441066a08c8963@ec2-54-247-85-251.eu-west-1.compute.amazonaws.com:5432/d524f86431l6o8'

DATABASE_CONNECT_OPTIONS = {}

# Suppress warning
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for signing the data. 
CSRF_SESSION_KEY = "de43cb1de1d68845beaf5d05"

# Secret key for signing cookies
SECRET_KEY = "c7f703f26e32c0ba4ccd9ab1"