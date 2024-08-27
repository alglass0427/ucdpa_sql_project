from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))   # C:Users/.../..../....
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)   # Bind the SQLAlchemy object to the app instance
    with app.app_context():
        db.create_all()
    return app

   