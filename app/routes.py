from flask import render_template, redirect, url_for, request, session, flash, jsonify
from flask import current_app as app
from werkzeug.security import generate_password_hash
from functools import wraps
import functions.functions as func    ###Functions file in functions folder to seperate functions from app.py
import functions.stock_functions as stock_func    ###Functions file in functions folder to seperate functions from app.py
import functions.mail_functions as mail_func    ###Functions file in functions folder to seperate functions from app.py
# import os
# import json
from .models import UserDetails, Portfolio , Asset, portfolio_assets # Import models
from . import db  # Import the db instance
# from flask_login import login_user

###Main App below

# Login required decorator to ensure usure is in session
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        rule = str(request.url_rule)
        print(f"route is {str(rule)}")
        print(rule == "/") 
        print(type(str(rule)))
        # print(session['email'])
        if rule ==  "/":
            if 'username' in session:
                flash(f"Logged in as , {session['username']}","success")
        elif 'username' not in session:
            flash("Please log in first", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template('index.html')


# ----------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        
        # Check if the user already exists
        existing_user = UserDetails.query.filter_by(email=email).first()
        if existing_user:
            flash(f"{email} is already registered -  Please Log In!", 'warning')
            return redirect(url_for('login'))
        
        # Create a new user
        new_user = UserDetails(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
            # password_hash="testpassword"
        )
        
        # Add the user to the session and commit to the database
        db.session.add(new_user)
        db.session.commit()
        
        # Initialize an empty portfolio for the user (if necessary)
        new_portfolio = Portfolio(user_id=new_user.id)  # Optionally create an empty portfolio
        db.session.add(new_portfolio)
        db.session.commit()
        
        # Log the user in
        session['username'] = username
        session['email'] = email
        session['user_id'] = new_user.id
        mail_func.smtp_sendmail(email=email,message = f"Subject:Sign Up Success!\n\nCongratulations {username},\nYou have started your Equity portfolio!!")

        return redirect(url_for('dashboard_1'))
        #if the user does not exist then add to the JSON of users
     
    return render_template('signup.html')
#--------------------------


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

       # Query the database for the user by email
        user = UserDetails.query.filter_by(email=email).first()

        if user and user.check_password(password):  # Use the check_password method
            session['user_id'] = user.id  # Store user ID in session
            session['username'] = user.username  # Store username in session
            session['email'] = email  # Store email in session
            return redirect(url_for('dashboard_1'))  # Redirect to the dashboard
        else:
            flash('Invalid email or password', 'danger')  # Flash message for invalid credentials
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    print(session)
    session.pop('username', None)
    session.pop('email', None)
    flash("You have been logged out", "info")
    return redirect(url_for('index'))


@app.route('/dashboard_1',methods=['GET', 'POST'])
@login_required
def dashboard_1():
    yf_flag = request.args.get('yf_flag', 'off') 
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    
    print(f"Inside Dashboard Yahoo flag  - {yf_flag}")
    # Get the user's ID from the session
    user_id = session['user_id']

    # Fetch the user from the database
    user = UserDetails.query.get(user_id)

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('login'))

    # Fetch the user's portfolios and associated assets
    portfolios = Portfolio.query.filter_by(user_id=user_id).all()
    stocks_with_prices = []
    for portfolio in portfolios:
        for asset in portfolio.assets:
            stock_code = asset.ticker
            # Fetch the stock price
            stock_price = stock_func.get_stock_price(stock_code, yf_flag)
            # Fetch additional data stored in the portfolio_assets table
            asset_data = db.session.query(portfolio_assets).filter_by(portfolio_id=portfolio.id, asset_id=asset.id).all()
            ###removed To get multiple purchases 
            # asset_data = db.session.query(portfolio_assets).filter_by(portfolio_id=portfolio.id, asset_id=asset.id).first()
            for asset in asset_data:
                stocks_with_prices.append({
                    'stock_code': stock_code,
                    'buy_price': asset.buy_price,
                    'no_of_shares': asset.no_of_shares,
                    'stop_loss': asset.stop_loss,
                    'cash_out': asset.cash_out,
                    'comment': asset.comment,
                    'latest_price': stock_price
                })  

    print(f"This is the Stock data passed to the Dashboard ::::: {stocks_with_prices} ")

    return render_template('dashboard_1.html', username=user.username, stocks=stocks_with_prices)

# this will add the Stock then , update the list , 
# then call dashboard_1 which will get the updated list and get the prices 

@app.route('/add_stock', methods=['POST'])
def add_stock():
    # EXISTING ------------------------
    print("INSIDE ADD STOCK")
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    yf_flag = 'off'
    ##Change for loop
    username = session['email']
    user_id = session['user_id']
    stock_code = request.form['stock_code']
    buy_price = float(request.form['buy_price'])
    no_of_shares = int(request.form['no_of_shares'])
    stop_loss = float(request.form['stop_loss'])
    cash_out = float(request.form['cash_out'])
    comment = request.form['comment']
    # END EXISTING ------------------------
    # Retrieve the user and portfolio
    user = UserDetails.query.get(user_id)
    portfolio = Portfolio.query.filter_by(user_id=user_id).first()

    if not portfolio:
        portfolio = Portfolio(user_id=user_id)
        db.session.add(portfolio)
        db.session.commit()

    # Check if the asset already exists
    asset = Asset.query.filter_by(ticker=stock_code).first()

    if not asset:
        asset = Asset(ticker=stock_code)
        db.session.add(asset)
        db.session.commit()

    # Insert the stock details into the portfolio_assets table
    # Get the asset and portfolio IDs from your existing logic
    portfolio_id = portfolio.id
    asset_id = asset.id

    # Create a dictionary to hold the dynamic values
    dynamic_values = {
        'portfolio_id': portfolio_id,
        'asset_id': asset_id,
    }
    
    # List of expected fields in the form that map to the columns in `portfolio_assets`
    #safe guard Against the insert failure
    expected_fields = ['buy_price', 'no_of_shares', 'stop_loss', 'cash_out', 'comment']

    for key, value in request.form.items():
        if key in expected_fields:
            dynamic_values[key] = value
            print(dynamic_values)
        elif key == 'yahooFinance':
            yf_flag = value
            print(f"Inside For  - {yf_flag}")
    # Now, create the insert statement using the dynamic_values dictionary
    stmt = portfolio_assets.insert().values(**dynamic_values)

    print(stmt)
    db.session.execute(stmt)
    db.session.commit()

    flash(f'Stock {stock_code} added to your portfolio.', 'success')

    return redirect(url_for('dashboard_1', yf_flag=yf_flag))

@app.route('/remove_stock/<string:stock_code>')
def remove_stock(stock_code):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['email']
    user_data = stock_func.load_user_portfolio(username)

    if stock_code in user_data:
        user_data.pop(stock_code)
        stock_func.save_user_portfolio(username, user_data)
    
    return redirect(url_for('dashboard_1'))


# new Redirect For 404 Error 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


###practice For passing between templates
@app.route('/validator')
def validator():
    lower_letter = False
    upper_letter = False
    num_end = False
    report = False
    user_exists = False

        # password = request.form['password']
    accounts = stock_func.load_user_accounts()
        


    # try:
    username = request.args.get("username")
    print(username)
    
        
        

    if username != "":
        lower_letter = any(c.islower() for c in username)
        if username in accounts:
            user_exists = True 
        ##short hand for looping through user name
        # for letter in username:
        #     if letter.lower() == letter:
        upper_letter = any(c.isupper() for c in username)
        num_end =  username[-1].isdigit()

        report = lower_letter and upper_letter and num_end and user_exists

    return render_template('validator.html', report = report , lower = lower_letter , upper = upper_letter, num_end = num_end, user_exists = user_exists)
    # except TypeError:
    #     print("No Users Exist!!!")



# if __name__ == '__main__':
#     app.run(debug=True)
