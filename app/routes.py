from flask import render_template, redirect, url_for, request, session, flash, jsonify
from flask import current_app as app
from flask_babel import Babel
from werkzeug.security import generate_password_hash 
from sqlalchemy.sql import func
from sqlalchemy import exc
from functions.stock_functions import yf
import functions.stock_functions as stock_func    ###Functions file in functions folder to seperate functions from app.py
import functions.mail_functions as mail_func    ###Functions file in functions folder to seperate functions from app.py
from flask_security import roles_required
from datetime import datetime
# import pytz
from sqlalchemy import exc
from .models import UserDetails, Portfolio , Asset, PortfolioAsset, Role, UserRole # Import models
# from flask_security import Security, SQLAlchemyUserDatastore

from . import db  # Import the db instance
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
login_manager = LoginManager(app)
login_manager.login_view = "login"
# user_datastore = SQLAlchemyUserDatastore(db, UserDetails, Role)
# security = Security(app, user_datastore)

# main page
@app.route('/')
def index():
    return render_template('index.html')

# assigned the log in manager
@login_manager.user_loader
def load_user(user_id):
    return UserDetails.query.get(int(user_id))

########################################################################################################################
##############SIGN UP USER   --->>> CREATE FIRST PORTFOLIO - - - FORM VALIDATIONS ON CLIENT SIDE########################
########################################################################################################################
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        portfolio_desc = request.form['portfolio_desc']
        seed_capital = request.form['seed_capital']
        
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
        )
        
        # Add the user to the session and commit to the database
        db.session.add(new_user)
        db.session.commit()
        
        # Initialize an empty portfolio for the user (if necessary)
        new_portfolio = Portfolio(
            user_id=new_user.id, 
            portfolio_desc = portfolio_desc )  # Optionally create an empty portfolio
        
        db.session.add(new_portfolio)
        db.session.commit()
        print(f"New Portfolio ID : {new_portfolio.id}")
################################################
        # Check if the asset already exists
        asset = Asset.query.filter_by(ticker="CASH").first()

        if not asset:
            asset = Asset(ticker="CASH",company_name="Cash",industry="Capital")
            db.session.add(asset)
            db.session.commit()
        else:
            asset = Asset.query.filter_by(ticker = "CASH").first()

      
        capital = PortfolioAsset(
                    portfolio_id=new_portfolio.id,
                    asset_id=asset.id,
                    no_of_trades = 1,
                    buy_price=seed_capital,
                    no_of_shares= 1,
                    holding_value = seed_capital,
                    stop_loss= 0,
                    cash_out= 0,
                    comment="Seed Capital"
        )
        db.session.add(capital)
        db.session.commit()
        # Log the user in
        login_user(new_user)
        mail_func.smtp_sendmail(email=email,message = f"Subject:Sign Up Success!\n\nCongratulations {username},\nYou have started your Equity portfolio!!")

        return redirect(url_for('portfolios'))
        #if the user does not exist then add to the JSON of users
     
    return render_template('signup.html')
#--------------------------
########################################################################################################################
##############LOG IN USER VIA USERMIXIN ######################################################################
########################################################################################################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print("LOGIN")
       # Query the database for the user by email
        user = UserDetails.query.filter_by(email=email).first()
        if user:
            print("User found")
        else:
            print("User not found")
        if user and user.check_password(password):  # Use the check_password method
            print("Password correct")
            login_user(user)
            print("User logged in")
            return redirect(url_for('dashboard_2'))  # Redirect to the dashboard
        else:
            print("User not found")
            flash('Invalid email or password', 'danger')  # Flash message for invalid credentials
            return redirect(url_for('login'))

    return render_template('login.html')

########################################################################################################################
##############LOG OUT USER ######################################################################
########################################################################################################################
@app.route('/logout')
@login_required
def logout():
    print(session)
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for('index'))

@app.route('/get_bid_offer', methods=['POST'])
def get_bid_offer():
    if request.method == 'POST':
        
        data = request.get_json() # retrieve the data sent from JavaScript
        print(f"Ticker : {data}")
        ticker = data['ticker']
        if ticker  ==  "":
            return jsonify({'last_quote': "NA" , "message": "Please Select a ticker to refresh prices!", "category": "success"})
    else:
        # If using a GET request, retrieve portfolio from the query string
        ticker = request.args.get('ticker')
    print(ticker)
    last_quote = stock_func.get_latest_price(ticker)
    # return jsonify({"message": "Asset added successfully!", "category": "success"}), 201
    return jsonify({'last_quote': last_quote , "message": "Asset added successfully!", "category": "success"})


###########MAIN DASHBOARD ROUTE  ######################################################################################
###########INSIDE THE DASHBOARD WILL RENDER THE RELEVENT SECTIONS ON DEMAND via dashboard_tbl##########################
########################################################################################################################
@app.route('/dashboard_2',methods=['GET', 'POST'])
@login_required
def dashboard_2():
    asset_list = Asset.query.all()
    portfolios = current_user.portfolios 
    return render_template('dashboard_2.html', username=current_user.username,  portfolios=portfolios,asset_list=asset_list)


###################################################################################
####ERROR PAGES 404 + 500
###################################################################################
# new Redirect For 404 Error 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

###################################################################################
####VALIDATOR
###################################################################################
###practice For passing between templates
@app.route('/validator', methods = ['GET', 'POST'])
def validator():
    print(request.method)
    if request.method == 'POST':
        email = request.form['val_email']
        
        print("LOGIN")
       # Query the database for the user by email
        existing_user = UserDetails.query.filter_by(email=email).first()
        if existing_user:
            print("VALID")
            flash(f"{email} is already registered -  Please Log In!", 'success')
        else:
            flash(f"{email} is not registered -  Please Sign Up!", 'warning')
            print("INVALID")
        return render_template('signup.html')
    return render_template('signup.html')
    # except TypeError:
    #     print("No Users Exist!!!")


###################################################################################
####PORTFOLIO SCREEN
###################################################################################
@app.route('/portfolios')
@login_required
def portfolios():
    current_user.username
    # Fetch the user's portfolio
    portfolio_list = Portfolio.query.filter_by(user_id=current_user.id).all()
    print (current_user.id)
    for user in portfolio_list:
        print(user.user_id)
        print(user.id)
    return render_template('portfolios.html',portfolios=portfolio_list)

###################################################################################
####ADD PORTFOLIO and INITIAL CAPITAL AMOUNT via - used CASH as An ASSET 
###################################################################################

@app.route('/add_portfolio', methods=['GET', 'POST'])
@login_required
def add_portfolio():
    cash = Asset.query.filter_by(ticker="CASH").first()
    if request.method == 'POST':
        portfolio_desc =  request.form['portfolio_desc']
        seed_capital =  request.form['seed_capital']
        # pass       
        if not Portfolio.query.filter_by(user_id=current_user.id,portfolio_desc = portfolio_desc).first():
            
            new_portfolio = Portfolio(user_id=current_user.id , portfolio_desc = portfolio_desc )
            db.session.add(new_portfolio)
            db.session.commit()
            capital = PortfolioAsset(
                    portfolio_id=new_portfolio.id,
                    asset_id=cash.id,
                    no_of_trades = 1,
                    buy_price=seed_capital,
                    no_of_shares= 1,
                    holding_value = seed_capital,
                    stop_loss= 0,
                    cash_out= 0,
                    comment="Seed Capital"
        )
                       
            # Optionally create an empty portfolio

            db.session.add(capital)
            db.session.commit()
            portfolio_list = Portfolio.query.filter_by(user_id=current_user.id).all()
            return render_template('portfolios.html', portfolios=portfolio_list)
        else:
            flash(f"Portfolio Name '{portfolio_desc}' already exists for user {current_user.username}.", "warning")
            return redirect('portfolios')


###################################################################################
####PORTFOLIO DATA with AGGREGATE FUNCTIONS  - - Common Table Expression(CTE USED for efficiency)
###################################################################################
@login_required
@app.route('/get_all_portfolios', methods=['POST'])
def get_all_portfolios():
    # Fetch all portfolios from the database
    print("Fetching portfolios...")
    data = request.get_json() # retrieve the data sent from JavaScript
    portfolio = data['portfolio']
    print(f" OUTSIDE : {portfolio}")
    portfolio_array = []
    # portfolios = Portfolio.query.all()
    # print(f"Portfolios: {portfolios}")

    # aggregated_assets_cte = db.session.query(
    #     Portfolio.id.label('portfolio_id'),
    #     Asset.company_name,
    #     func.sum(PortfolioAsset.holding_value).label('total_holding_value'),
    #     func.sum(PortfolioAsset.no_of_trades).label('total_no_of_trades')  # Aggregate no_of_trades
    # ).outerjoin(Portfolio.portfolio_assets)\
    #     .outerjoin(PortfolioAsset.asset) \
    #     .filter(Portfolio.user_id == current_user.id , Asset.company_name != "CASH") \
    # .group_by(Portfolio.id,Asset.company_name).cte('aggregated_assets')
    # test  = db.session.query(aggregated_assets_cte).all()
    # print(test)

    if portfolio != 'All':
        all_details_cte = db.session.query(
        Portfolio.id.label('portfolio_id'),
        Portfolio.portfolio_desc,
        Asset.ticker,
        Asset.company_name,
        Asset.industry,
        PortfolioAsset.no_of_trades,
        PortfolioAsset.holding_value,
        UserDetails.username,  # Assuming you have a User model related to Portfolio
        UserDetails.id.label('user_id')  # Assuming you have a User model related to Portfolio
            ).outerjoin(Portfolio.portfolio_assets)\
                .outerjoin(PortfolioAsset.asset)\
                .outerjoin(UserDetails, UserDetails.id == current_user.id) \
                    .filter(Portfolio.portfolio_desc == portfolio).cte('all_details')
        print ("SINGLE QUERY")
        # test  = db.session.query(aggregated_assets_cte).all()
        # print(test)

    else:
    # Step 1: Define CTE for all portfolio details (portfolio, assets, user details, etc.)
        all_details_cte = db.session.query(
            Portfolio.id.label('portfolio_id'),
            Portfolio.portfolio_desc,
            Asset.ticker,
            Asset.company_name,
            Asset.industry,
            PortfolioAsset.no_of_trades,
            PortfolioAsset.holding_value,
            UserDetails.username,  # Assuming you have a User model related to Portfolio
            UserDetails.id.label('user_id') 
        ).outerjoin(Portfolio.portfolio_assets)\
            .outerjoin(PortfolioAsset.asset)\
                .outerjoin(UserDetails, UserDetails.id == current_user.id )\
                    .filter(Portfolio.user_id  == current_user.id).cte('all_details')
        print ("ALL QUERY")
        # test  = db.session.query(aggregated_assets_cte).all()
        # print(test)            

    # Step 2: Define CTE for maximum trades
    max_trades_cte = db.session.query(
        all_details_cte.c.portfolio_id,
        func.coalesce(func.sum(all_details_cte.c.no_of_trades), 0).label('max_trades') \
    ).filter(all_details_cte.c.ticker != "CASH")\
        .group_by(all_details_cte.c.portfolio_id).cte('max_trades')

    test  = db.session.query(max_trades_cte).all()
    print(f"N : {test}")
    # Step 3: Define CTE for total investments
    total_investments_cte = db.session.query(
        all_details_cte.c.portfolio_id,
        func.count(all_details_cte.c.portfolio_id).label('total_investments')
    ).filter(all_details_cte.c.ticker != "CASH")\
        .group_by(all_details_cte.c.portfolio_id).cte('total_investments')

    test  = db.session.query(total_investments_cte).all()
    print(f"Total Investments : {test}")

        # Step 3: Define CTE for total investments
    sum_investments_cte = db.session.query(
        all_details_cte.c.portfolio_id,
        func.sum(all_details_cte.c.holding_value).label('sum_investments') \
    ) .filter(all_details_cte.c.ticker != "CASH")\
        .group_by(all_details_cte.c.portfolio_id).cte('sum_investments')
    
            # Step 3: Define CTE for total investments
    sum_cash_cte = db.session.query(
        all_details_cte.c.portfolio_id,
        func.sum(all_details_cte.c.holding_value).label('sum_cash') \
    ) .filter(all_details_cte.c.ticker == "CASH")\
        .group_by(all_details_cte.c.portfolio_id).cte('sum_cash')

    test  = db.session.query(sum_investments_cte).all()
    print(f"Sum Investments : {test}")


    # agg  = db.session.query(
    #         all_details_cte.portfolio_id

    # Step 4: Combine all the CTEs and fetch distinct portfolios with related data
    final_query = db.session.query(
        all_details_cte.c.portfolio_id,
        all_details_cte.c.portfolio_desc,     
        func.coalesce(total_investments_cte.c.total_investments, 0).label('total_investments'),
        func.coalesce(max_trades_cte.c.max_trades, 0).label('max_trades'),
        func.coalesce(sum_investments_cte.c.sum_investments, 0).label('sum_investments'),
        func.coalesce(sum_cash_cte.c.sum_cash, 0).label('sum_cash')
    ).outerjoin(max_trades_cte, all_details_cte.c.portfolio_id == max_trades_cte.c.portfolio_id) \
    .outerjoin(total_investments_cte, all_details_cte.c.portfolio_id == total_investments_cte.c.portfolio_id) \
    .outerjoin(sum_investments_cte, all_details_cte.c.portfolio_id == sum_investments_cte.c.portfolio_id) \
    .outerjoin(sum_cash_cte, all_details_cte.c.portfolio_id == sum_cash_cte.c.portfolio_id) \
    .filter(all_details_cte.c.user_id == current_user.id) \
    .distinct(all_details_cte.c.portfolio_id)  # Distinct portfolios

    # Step 5: Execute the query
    portfolios = final_query.all()
    print(f"ALL PORTFOLIOS {portfolios}")
    # Handling the result
    for portfolio in portfolios:
        print(f"Portfolio ID: {portfolio.portfolio_id}, Description: {portfolio.portfolio_desc}")
        print(f"Total Investments: {portfolio.total_investments}, Max Trades: {portfolio.max_trades}")

    # Fetch portfolio assets for drill-down details


    if portfolios:
        # Render the table rows for all portfolios
        return render_template('portfolio_rows.html', portfolios=portfolios ,  all_details = db.session.query(all_details_cte).all() )
    else:
        return jsonify({"error": "No portfolios found"}), 404


@login_required
@app.route('/get_portfolio_data', methods=['POST'])
def get_portfolio_data():
    if not current_user.is_authenticated:
        return jsonify({"error": "User not authenticated"}), 401  # 401 Unauthorized
    portfolio_id = request.form['portfolio_id']
    portfolio = Portfolio.query.filter_by(id=portfolio_id).first()
    return render_template('portfolio_rows.html', portfolios=[portfolio])


########################################################################################################
########DASHBOARD ASSETS PER PORTFOLIO IN MAIN TABLES ##################################################
########################################################################################################

@app.route('/get_portfolio_assets', methods=['GET','POST'])
def get_portfolio_assets():
    if not current_user.is_authenticated:
        return jsonify({"error": "User not authenticated"}), 401  # 401 Unauthorized
    
    if request.method == 'POST':
        data = request.get_json() # retrieve the data sent from JavaScript
        portfolio = data['portfolio']
        yf_flag = data['yf_flag']
    else:
        # If using a GET request, retrieve portfolio from the query string
        portfolio = request.args.get('portfolio')
        yf_flag = request.args.get('yf_flag')
    
    print(portfolio)
    cash_asset = Asset.query.filter_by(ticker="CASH").first()
    cash = PortfolioAsset.query.join(Portfolio).filter(
    PortfolioAsset.asset_id == cash_asset.id,  # Filter for "CASH" asset
    Portfolio.portfolio_desc == portfolio,  # Filter by portfolio description
    Portfolio.user_id == current_user.id  # Filter by user (assuming user_id is in the Portfolio model)
        ).first()
    print(f"Cash in filter_by =  {cash}")

    print("Fetching portfolio assets...in get_porfolio_assets")
    assets = db.session.query(Portfolio, PortfolioAsset, Asset).\
                        outerjoin(Portfolio.portfolio_assets).\
                        outerjoin(PortfolioAsset.asset).\
                        filter(Portfolio.portfolio_desc == portfolio).all()
    print(f"Assets : {assets}")
    # print(f"Portfolio ID from Assets : {assets[0][0]}")
    print(f"Yahoo Flag : {yf_flag}")
    if yf_flag == 'on':
        for portfolio, portfolio_asset, asset in assets:
            if asset.ticker != "CASH":
                print(f"Asset in ASSET LOOP BEFORE STOCK FUNCTION: {portfolio_asset}")
                print(f"ALL YAHOO TICKER: {asset.ticker}")
                print(f"ALL YAHOO PORTFOLIO: {asset.id}")   
                print(f"ALL YAHOO BUY PRICE: {portfolio_asset.buy_price}")
                all_yahoo =  stock_func.get_stock_price(stock_code = asset.ticker, 
                                                        asset_id = asset.id, 
                                                        portfolio=assets[0][0].id , 
                                                        yf_flag = yf_flag ,
                                                        user_id  = current_user.id, 
                                                        buy_price = portfolio_asset.buy_price)
            
                print(f"ALL YAHOO : {all_yahoo}")
                portfolio_asset.latest_price = all_yahoo[1]
                    
    else:
        latestprices =  stock_func.get_latest_portfolio_prices(portfolio=assets[0][0].id)
        for portfolio, portfolio_asset, asset in assets:
            if asset.ticker != "CASH":
                if asset.ticker in latestprices:
                    latest_price = latestprices[asset.ticker]
                    # Dynamically add the latest_price attribute to the portfolio_asset object
                    portfolio_asset.latest_price = latest_price
                    print(f"Latest Price for {asset.ticker}: {portfolio_asset.latest_price}")
                else:
                    # If no latest price is available, you can set it to None or 0
                    portfolio_asset.latest_price = None
                    print(f"No latest price available for {asset.ticker}")


    # Check if the ticker exists in the latest prices and append it to the portfolio_asset object
        
        
        # for ast in portfolio_asset:
        #     print(f"Asset innner loop {ast}")
    
    
    if portfolio:
        print(portfolio)
        # Render the table rows for all portfolios
        return render_template('dashboard_tbl.html', stocks=assets , cash = cash)
    else:
        return jsonify({"error": "No portfolios found"}), 404

###################################################################################
##POPLATE CARDS HTML for DASHBOARD   --->>>   HIDDEN UNTIL SMALL SCREEN SIZE --->>> REMOVE -  MOVED TO TABLE
###################################################################################


###################################################################################
###POPULATE THE DROPDOWN IN DASHBOARD FOR ADDING TO PORTFOLIO
###################################################################################


@app.route('/get_asset_list_api', methods=['POST'])
def get_asset_list_api():
    asset_list = Asset.query.order_by(Asset.ticker.asc()).all()
    print(asset_list[0].ticker)  # Just to confirm it's working
    return jsonify([asset.to_json() for asset in asset_list])  # Send JSON response


###################################################################################
####ADMIN   
###################################################################################

@app.route('/admin_maintain', methods = ['POST'])
def admin_maintain():

    ADMIN_MAINTAIN_PASSWORD = 'supersecretpassword'
    if request.method == 'POST':
        entered_password = request.form.get('admin_password')
        if entered_password == ADMIN_MAINTAIN_PASSWORD:
            user_list = UserDetails.query.order_by(UserDetails.username.asc()).all()
            role_list = Role.query.order_by(Role.name.asc()).all()
            # Password is correct, grant access
            return render_template('admin_maintain.html', users=user_list ,  roles = role_list)
        else:
            # Password is incorrect, show an error
            flash('Invalid admin password', 'danger')
            return redirect(url_for('login'))
        

###################################################################################
####ADD USER ACCESS ROLES
###################################################################################

@app.route('/admin_maintain_action', methods=['POST'])
def admin_maintain_action():
    if request.method == 'POST':
        role_form =  request.form['role']
        user_form =  request.form['userName']
        user = UserDetails.query.filter_by(username = user_form).first()
        role = Role.query.filter_by(name = role_form).first()
        # userrole = UserRole.query.filter_by(name= role).first()
        print (user.roles)
        if user.roles:
            user.roles.roll_id = role.id
        else:
            user.roles.append (role)
        try:
            db.session.commit()
            flash(f"User Role Updated! - User Name : {user_form} is now Role : {role_form}", 'success')
        except exc.IntegrityError as e:
            db.session.rollback()
            flash(f"Error : {e}", 'danger')
        
    user_list = UserDetails.query.order_by(UserDetails.username.asc()).all()
    role_list = Role.query.order_by(Role.name.asc()).all()
    return render_template('admin_maintain.html', users=user_list ,  roles = role_list)

@login_required
@app.route('/admin')
def admin():
    all_assets = Asset.query.all()
    return render_template('admin.html', assets = all_assets)

###################################################################################
####ADMIN  --->>> ADD ASSET TO ASSET DATA STATIC TABLE
###################################################################################
@login_required
@app.route('/add_asset', methods=['POST'])
def add_asset():
    

    try:
        # Parse the incoming JSON data from the request body
        data = request.get_json()

        # Extract asset details
        ticker = data.get('ticker')
        company_name = data.get('company_name')
        industry = data.get('industry')

        # Create a new Asset object and add it to the database
        new_asset = Asset(ticker=ticker, company_name=company_name, industry=industry)
        db.session.add(new_asset)
        db.session.commit()

        # Return success response
        return jsonify({"message": "Asset added successfully!", "category": "success"}), 201
    except Exception as e:
        # Handle any exceptions that may occur
        return jsonify({"error": str(e)}), 400
    

###################################################################################
####ADD STOCK FROM DASHBOARD
###################################################################################
@app.route('/add_stock_db', methods=['POST'])
def add_stock_db():
    try:

        data = request.get_json()
        # Extract asset details
        stock_code = data.get('stock_code')
        buy_price = data.get('buy_price')
        no_of_shares = data.get('no_of_shares')
        stop_loss = data.get('stop_loss')
        cash_out = data.get('cash_out')
        comment = data.get('comment')
        portfolio_name = data.get('portfolioName')
        portfolio = Portfolio.query.filter_by(user_id = current_user.id,portfolio_desc=portfolio_name).first()
        print(portfolio.user_id)
        # portfolio = Portfolio.query.filter_by(portfolio_desc=portfolio_name).first()
        
        cash = Asset.query.filter_by(ticker = "CASH").first()
        capital = PortfolioAsset.query.filter_by(portfolio_id = portfolio.id,asset_id = cash.id).first()

        if capital.holding_value < (float(buy_price) * float(no_of_shares)):
            return jsonify({"message": "Not Enough Capital - (Buy Price * Volume > Capital (Cash)!", "category": "danger"}), 201
            
        if not portfolio:
           
            return jsonify({"message": "No Portfolio Exists with this Description!","category": "danger"}), 201

        # Check if the asset already exists
        asset = Asset.query.filter_by(ticker=stock_code).first()

        if not asset:
            # asset = Asset(ticker=stock_code)
            # db.session.add(asset)
            # db.session.commit()
            return jsonify({"message": "No Asset with this Ticker - Contact Admin!","category": "danger"}), 201

#######Reduce Cash###############

        # Retrieve the user and portfolio
        # Insert the stock details into the portfolio_assets table
        # Get the asset and portfolio IDs from your existing logic

        if portfolio and asset:
            holding = PortfolioAsset.query.filter_by(portfolio_id = portfolio.id,asset_id = asset.id).first()
            
            print(f" Holding Price : {holding}")
            if holding :
                holding.no_of_trades = int(holding.no_of_trades)+1
                holding.buy_price = float(buy_price)
                holding.no_of_shares = (float(holding.no_of_shares) + float(no_of_shares))
                holding.holding_value = (float(holding.holding_value) + (float(buy_price) * float(no_of_shares)))
                db.session.commit()
                capital.holding_value  = round((capital.holding_value - (float(buy_price) * float(no_of_shares))),2)
                db.session.commit()

            else:
                portfolio_asset = PortfolioAsset(
                    portfolio_id=portfolio.id,
                    asset_id=asset.id,
                    no_of_trades = 1,
                    buy_price=buy_price,
                    no_of_shares=no_of_shares,
                    holding_value = (float(buy_price) * float(no_of_shares)),
                    stop_loss=stop_loss,
                    cash_out=cash_out,
                    comment=comment
            )
                      
            # Add the new PortfolioAsset record to the session and commit
                db.session.add(portfolio_asset)
                capital.holding_value  = round((capital.holding_value - (float(buy_price) * float(no_of_shares))),2)
            try:
                # db.session.commit()
                
                db.session.commit()
                return jsonify({"message": f"Bought Equity : {stock_code} (Buy Price : {buy_price}) , Cost : {(float(buy_price) * float(no_of_shares))} ", "category": "success"}), 201
                # flash("Stock added to portfolio successfully.", "success")
            except exc.IntegrityError as e:
                db.session.rollback()
                return jsonify({"message": "Something Went Wrong - Rolled Back Change!", "category": "danger"}), 201
          
        # Return success response
        
    except Exception as e:
        # Handle any exceptions that may occur
        return jsonify({"error": str(e)}), 400


###################################################################################
####PORTFOLIO SCREEN  -->>> REMOVE STOCK FROM RELATED PORTFOLIO  
##### --> ASSIGNED VIA URL WHEN RENDERING THE TABLE in DASHBOARD
##### -->
###################################################################################

@login_required
@app.route('/remove_stock/<string:stock_code>', methods = ['POST'])
def remove_stock(stock_code):
    portfolio_id = request.args.get('portfolio_id')  # Get portfolio_id from query string
    print (portfolio_id)

    cash = Asset.query.filter_by(ticker = "CASH").first()
    capital = PortfolioAsset.query.filter_by(portfolio_id = portfolio_id,asset_id = cash.id).first()
    # Fetch the user's portfolio
    # portfolio = Portfolio.query.filter_by(user_id=user_id).first()
    print(f"Portfolio to BE DELETED frOM: {portfolio_id}")

  

    # Fetch the asset corresponding to the stock code
    asset = Asset.query.filter_by(ticker=stock_code).first()
    print(f"ASSET : {asset}")

    if not asset:
        # flash(f"Stock with ticker {stock_code} not found.", "danger")
        return jsonify({"message": f"Stock with ticker {stock_code} not found.", "category": "danger"}), 201

    # Fetch the specific PortfolioAsset entry
    portfolio_asset = PortfolioAsset.query.filter_by(portfolio_id=portfolio_id, asset_id=asset.id).first()
    
    try:
        sell_price  =  round(stock_func.get_latest_price(ticker = stock_code),2)
    except:
        sell_price = round(portfolio_asset.buy_price,2)


    if not portfolio_asset:
        # flash(f"Stock {stock_code} is not part of the portfolio.", "warning")
        return jsonify({"message": f"Stock {stock_code} is not part of the portfolio." , "category": "danger"}), 201


    # Remove the PortfolioAsset entry and add value from asset to capital
    capital.holding_value = round((float(capital.holding_value) + float(sell_price * portfolio_asset.no_of_shares)))
    db.session.delete(portfolio_asset)
    
    try:
        db.session.commit()
        #Handle te Flash response
        message  = (f"Sold Equity : {stock_code} (Trade Price : {sell_price}) , Value : {(float(sell_price) * float(portfolio_asset.no_of_shares))}")
        return jsonify({"message": message,"category": "success"}), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        message  = (f" Could not remove {stock_code} - Please try again later!")
        return jsonify({"message": message,"category": "danger"}) ,201
    

###################################################################################
####SELL SOMe OF THE STOCK VOLUME FROM DASHBOARD - - 
###################################################################################

@app.route('/sell_partial_db', methods=['POST'])
def sell_partial_db():
    try:

        data = request.get_json()
        # Extract asset details
        stock_code = data.get('stock_code')
        buy_price = data.get('buy_price')
        no_of_shares = data.get('no_of_shares')
        stop_loss = data.get('stop_loss')
        cash_out = data.get('cash_out')
        comment = data.get('comment')
        portfolio_name = data.get('portfolioName')
        portfolio = Portfolio.query.filter_by(user_id = current_user.id,portfolio_desc=portfolio_name).first()
        print(portfolio.user_id)
        
        cash = Asset.query.filter_by(ticker = "CASH").first()
        capital = PortfolioAsset.query.filter_by(portfolio_id = portfolio.id,asset_id = cash.id).first()
            
        if not portfolio:
           
            return jsonify({"message": "No Portfolio Exists with this Description!","category": "danger"}), 201

        # Check if the asset already exists
        asset = Asset.query.filter_by(ticker=stock_code).first()

        if not asset:
            
            return jsonify({"message": "No Asset with this Ticker - Contact Admin!","category": "danger"}), 201

#######INCREASE Cash  ################

        # Retrieve the user and portfolio
        # Insert the stock details into the portfolio_assets table
        # Get the asset and portfolio IDs from your existing logic

        if portfolio and asset:
            holding = PortfolioAsset.query.filter_by(portfolio_id = portfolio.id,asset_id = asset.id).first()

        if not holding:
            return jsonify({"message": "This Portfolio does not contain this Asset","category": "danger"}), 201
        if int(holding.no_of_shares) < int(no_of_shares):
            return jsonify({"message": "Not Enough Shares to Sell -  Change Volume!","category": "danger"}), 201
        if int(holding.no_of_shares) == int(no_of_shares):
            return jsonify({"message": "Volume = Remaining Shares  - Use Sell button on Asset","category": "danger"}), 201
      
        print(f" Holding Price : {holding}")
        
        if holding :
                holding.no_of_trades = int(holding.no_of_trades)+1
                holding.buy_price = float(buy_price)
                holding.no_of_shares = (float(holding.no_of_shares) - float(no_of_shares))
                holding.holding_value = (float(holding.holding_value) - (float(buy_price) * float(no_of_shares)))
                capital.holding_value  = round((capital.holding_value + (float(buy_price) * float(no_of_shares))),2)
                

        else:
                return jsonify({"message": "This Portfolio does not contain this Asset","category": "danger"}), 201
                              
            # Add the new PortfolioAsset record to the session and commit
           
        try:
            db.session.commit()
            return jsonify({"message": f"Bought Equity : {stock_code} (Sell Price : {buy_price}) , Value : {(float(buy_price) * float(no_of_shares))} ", "category": "success"}), 201
        except exc.IntegrityError as e:
            db.session.rollback()
            return jsonify({"message": "Something Went Wrong - Rolled Back Change!", "category": "danger"}), 201
            
        
    except Exception as e:
        # Handle any exceptions that may occur
        return jsonify({"error": str(e)}), 400




#TODO: add this 15min timer back in 
############## CAUSING ISSUE  --->>> LAST ACTIVITY AND CURRENT TIME NOT LINING UP- - - FORM VALIDATIONS ON CLIENT SIDE ## ##
########################################################################################################################
# @app.before_request
# def make_session_permanent():
#     session.permanent = True


# @app.before_request
# def check_session_timeout():
#     if current_user.is_authenticated:
#         # Get the current UTC time
#         current_time = datetime.now(pytz.utc)
        
#         # Check if 'last_activity' is in session
#         if 'last_activity' in session:
#             last_activity = session['last_activity']  # This should be a UTC-aware datetime
#             # Check if the difference is greater than 15 minutes

#             if (current_time - last_activity).total_seconds() > 15 * 60:  # 15 minutes
#                 logout_user()  # Log the user out
#                 return redirect(url_for('login'))  # Redirect to the login page

#         # Update last_activity in session
#         session['last_activity'] = current_time  # Store current time as UTC aware