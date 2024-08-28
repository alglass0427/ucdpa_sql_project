from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # basedir = os.path.abspath(os.path.dirname(__file__))   # C:Users/.../..../....
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Holly#040115@localhost/portfolio_db'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alwglass:G4MaiivKjlB6fpgdbD9WlHLlgeDBPCr9@dpg-cr735l3tq21c73f800cg-a.oregon-postgres.render.com/portfolio_db_5uxo'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'mysecretkey'
    CURRENT_DIR =  os.getcwd()
    # PERSISTENT_DIR =  os.path.join(CURRENT_DIR, 'persistent')
    # USER_DATA_FOLDER = os.path.join(PERSISTENT_DIR, 'users')
    # ACCOUNTS_FILE = os.path.join(PERSISTENT_DIR, 'accounts', 'accounts.json')
    db.init_app(app)

    with app.app_context():
        # Import routes, models, etc.
        from . import routes  # Import routes
        from .models import UserDetails, Portfolio, PortfolioAsset,Asset  # Import models

        db.create_all()  # Create database tables

    return app
