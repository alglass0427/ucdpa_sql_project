import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Pulls from Render's environment variables
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')  # Database URL from Render
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Holly#040115@localhost/portfolio_db'  # Database LOCAL
    # SECRET_KEY = 'secretkey'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('FLASK_DEBUG', False)  # Optionally enable debug mode
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)
    CURRENT_DIR =  os.getcwd()

