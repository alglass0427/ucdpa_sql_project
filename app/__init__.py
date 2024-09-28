from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
# from insert import import_assets_from_csv
# from insert_roles import add_roles
# from datetime import timedelta
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = app.config['SECRET_KEY']
    db.init_app(app)

    with app.app_context():
        # Import routes, models, etc.
        from . import routes  # Import routes
        from .models import UserDetails, Portfolio, PortfolioAsset,Asset,Role,UserRole  # Import models
        db.create_all()  # Create database tables        

    return app
