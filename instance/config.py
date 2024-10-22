import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True if os.getenv('DEBUG') == 'True' else False
TESTING = True if os.getenv('TESTING') == 'True' else False
FLASK_ENV = os.getenv('FLASK_ENV')
FLASK_APP = os.getenv('FLASK_APP')
FLASK_DEBUG = True if os.getenv('FLASK_DEBUG') == 'True' else False
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
