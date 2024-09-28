import os
from datetime import timedelta



class Config:

    basedir = os.path.abspath(os.path.dirname(__file__))   # C:Users/.../..../....
    SECRET_KEY = os.environ.get('SECRET_KEY','secretkey')  # Pulls from Render's environment variables
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI','sqlite:///'+os.path.join(basedir,'data.sqlite'))  # Database URL from Render
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Holly#040115@localhost/portfolio_db'  # Database LOCAL
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('FLASK_DEBUG', False)  # Optionally enable debug mode
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)
    CURRENT_DIR =  os.getcwd()

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
