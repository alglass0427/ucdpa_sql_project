from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from functools import wraps
import functions.functions as func    ###Functions file in functions folder to seperate functions from app.py
import functions.stock_functions as stock_func    ###Functions file in functions folder to seperate functions from app.py
import functions.mail_functions as mail_func    ###Functions file in functions folder to seperate functions from app.py
import os
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship




app = Flask(__name__)
app.secret_key = 'mysecretkey'
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Holly#040115@localhost/portfolio_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize the database
db = SQLAlchemy(app)

CURRENT_DIR =  os.getcwd()
PERSISTENT_DIR =  os.path.join(CURRENT_DIR, 'persistent')
USER_DATA_FOLDER = os.path.join(PERSISTENT_DIR, 'users')
ACCOUNTS_FILE = os.path.join(PERSISTENT_DIR, 'accounts', 'accounts.json')




# Ensure directories exist
# print(f"Creating user data folder at {USER_DATA_FOLDER}")
if not os.path.exists(USER_DATA_FOLDER):
    print(f"Creating user data folder at {USER_DATA_FOLDER}")
    os.makedirs(USER_DATA_FOLDER)


if not os.path.exists(os.path.dirname(ACCOUNTS_FILE)):
    print(f"Creating accounts directory at {ACCOUNTS_FILE}")
    os.makedirs(os.path.dirname(ACCOUNTS_FILE))

if not os.path.exists(ACCOUNTS_FILE):
    with open(ACCOUNTS_FILE, 'w') as f:
        print(f"Creating accounts file at {ACCOUNTS_FILE}")
        json.dump({}, f)  # Initialize with an empty dictionary


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
    #check if The user exists already
    if request.method == 'POST':
        username = request.form['fullname']
        email = request.form['email']
        # password = request.form['password']
        accounts = stock_func.load_user_accounts()
        
        if email in accounts:
            flash(f"{email} is already registered -  Please Log In!", 'warning')
            return redirect(url_for('login'))
        
        user_details =  {}
        for key, value in request.form.items():            
            user_details[key] = value
            print(user_details)
 
        

        
        accounts[email] = user_details
        # accounts[username] = username
        print(f"Details for {accounts[email] }")

        stock_func.save_user_accounts(accounts)
        # stock_func.save_user_portfolio(email, [])
        stock_func.save_user_portfolio(email, {})
        session['username'] = username
        session['email'] = email
        
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

        accounts = stock_func.load_user_accounts()
        # print(f" load user accounts function : accounts are , {accounts[username]} ")
        
        if email in accounts and accounts[email]["password"] == password:
            session['email'] = email
            session['username'] = accounts[email]["fullname"]
            return redirect(url_for('dashboard_1'))
        else:
            flash('Invalid username or password', 'danger')
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
    print("")
    yf_flag = request.args.get('yf_flag', 'off')  # 'off' is the default value
    
    if 'username' not in session:
        return redirect(url_for('login'))
    print(f"Inside Dashboard Yahoo flag  - {yf_flag}")
    username = session['username']
    email = session['email']
    user_data = stock_func.load_user_portfolio(email)
    print(f"User Data:{user_data}")
    
    # Fetch the prices for all stocks in the user's portfolio
    #stock_func.get_stock_price(stock)
    ##BACKWARDS FOR LOOP get the stock and the price for each stock in the portfolio
    #Seperate this to get the response in one API Call
    # stocks_with_prices = [(stock, "") for stock in user_data['portfolio']]
    # stock_func.get_stock_price(stock)

    stocks_with_prices = [(stock,user_data,stock_func.get_stock_price(stock,yf_flag)) for stock in user_data]
    print(f"This is the Stock data passed to the Dashboard ::::: {stocks_with_prices} ")

    return render_template('dashboard_1.html', username=username, stocks=stocks_with_prices)

# this will add the Stock then , update the list , 
# then call dashboard_1 which will get the updated list and get the prices 

@app.route('/add_stock', methods=['POST'])
def add_stock():
    print("INSIDE ADD STOCK")
    if 'username' not in session:
        return redirect(url_for('login'))
    # yf_flag = 'off'
    username = session['email']
    stock_code = request.form['stock_code'].upper()
    buy_price = request.form['buy_price']
    no_of_shares = request.form['no_of_shares']

    user_data = stock_func.load_user_portfolio(username)
    print(f"User Data:{user_data}")
    # if stock_code and stock_code not in user_data['portfolio']:
    if stock_code and stock_code not in user_data:
        stock_add_details =  {}
        # stock_add = {}
        for key, value in request.form.items():
            if key != 'yahooFinance':             
                stock_add_details[key] = value
                # print(f"-----------------")
                # print(f"Details To Add in /add Stock  - {stock_add_details}")
                # print(f"-----------------")
                user_data[stock_code] = stock_add_details
            else:
                yf_flag = value
                print(f"Inside For  - {yf_flag}")
            # print(f"Stock Add:{stock_add}")
            #Stock Add:{'B': {'stock_code': 'b', 'buy_price': 'b', 'no_of_shares': 'b'}}
        # user_data['portfolio'].append(stock_code)
        print(f"-----------------")
        print(f"Details To Add in /add Stock  - {user_data[stock_code]}")
        print(f"-----------------")
        print(f"Outside For  - {yf_flag}")
        if yf_flag == 'off':
            flash("Yahoo! Finance is off! - No latest prices displayed", "info")
        stock_func.save_user_portfolio(username, user_data)
    
    return redirect(url_for('dashboard_1',yf_flag = yf_flag))

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
    return render_template('404.html'), 500


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



if __name__ == '__main__':
    app.run(debug=True)
