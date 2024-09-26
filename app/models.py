from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy.orm import relationship
from app import db
import pytz
from flask_login import UserMixin
from flask_security import RoleMixin

class UserDetails(UserMixin, db.Model):
    __tablename__ = 'user_details'  # Specify the new table name
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) ### Is Foreign Key to User Role /  Portfolio / PortfolioAssets
    username = db.Column(db.String(150), unique=False, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))
    
    # Establish relationship with Portfolio
    portfolios = db.relationship('Portfolio', backref='owner', cascade="all, delete-orphan", lazy=True)
    roles = db.relationship('Role', secondary='user_roles', backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # def get_id(self):
    #     return str(self.id)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)   ### Is Foreign Key to User Role
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)   ###Primary 
    user_id = db.Column(db.Integer, db.ForeignKey('user_details.id'))  ###Foreign Key to create relationship to User Table
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  ###Foreign Key to create relationship to Roles Table



# Update the Portfolio and Asset models to use this mapped class
class Portfolio(db.Model):
    __tablename__ = 'portfolio'  # Specify the table name
    id = db.Column(db.Integer, primary_key=True)
    portfolio_desc = db.Column(db.String(150), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_details.id'), nullable=False)   ### User ID Foreign 
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))

    # Update the relationship to use the PortfolioAsset class
    portfolio_assets = db.relationship('PortfolioAsset', back_populates='portfolio', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'Portfolio ID: {self.id}  Portfolio Desc: {self.portfolio_desc} '
    

# Define the new ORM-mapped class for `portfolio_assets`
class PortfolioAsset(db.Model):
    __tablename__ = 'portfolio_assets'  # Specify the table name
    portfolio_asset_seq_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)   ### Asset ID Foreign  -  Addits managed by Admin roles
    no_of_trades = db.Column(db.Integer, nullable=False)
    # Additional fields from the form input
    buy_price = db.Column(db.Float, nullable=False)
    no_of_shares = db.Column(db.Integer, nullable=False)
    holding_value = db.Column(db.Float, nullable=True)
    stop_loss = db.Column(db.Float, nullable=True)
    cash_out = db.Column(db.Float, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    
    # New column to store the SVG content
    svg_content = db.Column(db.Text, nullable=True)
    # Define relationships back to Portfolio and Asset
    portfolio = db.relationship("Portfolio", back_populates="portfolio_assets")
    asset = db.relationship("Asset", back_populates="portfolio_assets")
   

class Asset(db.Model):
    __tablename__ = 'assets'  # Specify the table name
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), unique=True, nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(255), nullable=True)
    # Update the relationship to use the PortfolioAsset class
    
    def to_json(self):
        return {
            'id': self.id,
            'ticker': self.ticker,
            'company_name': self.company_name,
            'industry': self.industry
        }
    
    portfolio_assets = db.relationship('PortfolioAsset', back_populates='asset', cascade="all, delete-orphan")
    history = db.relationship('AssetHistory', backref='asset', lazy=True )   # cascade="all, delete-orphan"
    def __repr__(self):
        return f'<Asset {self.ticker}>'
    
class AssetHistory(db.Model):
    __tablename__ = 'asset_history'
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    open_price = db.Column(db.Float, nullable=True)
    high_price = db.Column(db.Float, nullable=True)
    low_price = db.Column(db.Float, nullable=True)
    close_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<AssetHistory {self.asset.ticker} - {self.date.strftime("%Y-%m-%d")}>'
    






    # ####relationship between portfolio And assets
# portfolio_assets = db.Table('portfolio_assets',
#     db.Column('portfolio_asset_seq_id', db.Integer, primary_key=True, autoincrement=True),
#     db.Column('portfolio_id', db.Integer, db.ForeignKey('portfolio.id'), primary_key=True),
#     db.Column('asset_id', db.Integer, db.ForeignKey('assets.id'), primary_key=True),
#     db.Column('buy_price', db.Float, nullable=False),
#     db.Column('no_of_shares', db.Integer, nullable=False),
#     db.Column('stop_loss', db.Float, nullable=True),
#     db.Column('cash_out', db.Float, nullable=True),
#     db.Column('comment', db.String(255), nullable=True)
# )



# class Portfolio(db.Model):

#     __tablename__ = 'portfolio'  # Name of the table
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user_details.id'), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))
#     # Establish the relationship with Asset using the association table
#     assets = db.relationship('Asset', secondary=portfolio_assets, back_populates='portfolios')

#     def __repr__(self):
#         return f'<Portfolio {self.id}>'

# class Asset(db.Model):
#     __tablename__ = 'assets'
#     id = db.Column(db.Integer, primary_key=True)
#     ticker = db.Column(db.String(10), unique=True, nullable=False)
#     portfolios = db.relationship('Portfolio', secondary=portfolio_assets, back_populates='assets')

# # Association table for the many-to-many relationship

# # class Asset(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     stock_ticker = db.Column(db.String(10), nullable=False)
# #     buy_price = db.Column(db.Float, nullable=False)
# #     no_of_shares = db.Column(db.Integer, nullable=False)
# #     stop_loss = db.Column(db.Integer, nullable=False)
# #     cash_out = db.Column(db.Integer, nullable=False)
# #     user_id = db.Column(db.Integer, db.ForeignKey('user_details.id'), nullable=False)
# #     created_at = db.Column(db.DateTime, default=datetime.now())



# # 1. Relationship Definition
# # relationship('Portfolio', backref='owner', lazy=True): This line defines a relationship between the User model and the Portfolio model.
# # 2. Parameters Explained
# # 'Portfolio': This is the name of the model that the User model is related to. In this case, User is related to Portfolio.

# # backref='owner':

# # backref creates a new property on the Portfolio model called owner, which refers back to the User who owns that portfolio.
# # This means you can access the user associated with a portfolio using something like portfolio.owner in your code.
# # Similarly, from a User instance, you can access all associated portfolios with user.portfolios.
# # lazy=True:

# # lazy determines how the related items are loaded from the database.
# # When lazy=True, SQLAlchemy will load the related items when you access them, i.e., it's a "lazy load."
# # This means that the related Portfolio objects will only be loaded from the database when you actually access user.portfolios.

# # 3. Practical Example
# # Let's say you have a user in your database, and you want to retrieve all the portfolios that belong to that user. Here's how you can use this relationship:

# # python
# # Copy code
# # # Assuming `user` is an instance of User
# # portfolios = user.portfolios  # This will give you a list of Portfolio objects related to this user

# # # Accessing the owner from a Portfolio object
# # for portfolio in portfolios:
# #     print(portfolio.owner.username)  # This will print the username of the user who owns the portfolio
# # 4. Bidirectional Relationship
# # Bidirectional Relationship: The backref creates a bidirectional relationship, meaning you can navigate the relationship from either side:
# # From User to Portfolio: user.portfolios
# # From Portfolio to User: portfolio.owner
# # 5. Summary
# # relationship('Portfolio', backref='owner', lazy=True) is used to link the User model with the Portfolio model.
# # It allows you to easily navigate between users and their portfolios, providing a clear and intuitive way to work with related data in your application.


# # In SQLAlchemy, if you do not explicitly define the __tablename__ attribute in your model class, SQLAlchemy will automatically create a default table name based on the name of the class. The default naming convention uses the lowercase version of the class name.

# # Default Behavior
# # Class Name to Table Name Mapping:

# # If you create a class named User, SQLAlchemy will automatically use user as the default table name.
# # If the class name is UserDetails, the default table name would be userdetails.
# # Example Without __tablename__:
