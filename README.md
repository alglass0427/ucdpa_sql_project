# ucdpa_python_project

## On Render
Link to deployment
https://ucdpa-sql-project.onrender.com/

## Portfolio Dashboard Flask Application with PostgreSQL
Overview
This is a Flask-based web application that allows users to manage a portfolio of stocks. The application enables users to add, remove, and view stocks in their portfolio. Additionally, the application fetches real-time stock prices and other data points (e.g., ISIN) using Yahoo Finance.

## Features
User Authentication: Secure login and session management.
Portfolio Management: Add, remove, and view stocks in your portfolio.
Real-time Data: Fetch live stock data using Yahoo Finance.
Responsive UI: A Bootstrap-based responsive interface that adapts to different screen sizes.

## Prerequisites
Before running this application, ensure you have the following installed:

Python 3.x
pip

Installation
## Clone the Repository
    git clone https://github.com/alglass0427/ucdpa_sql_project.git
    cd portfolio-dashboard
## Create and Activate a Virtual Environment
    Create a virtual environment to manage dependencies:
    python -m venv venv

        Activate the virtual environment:
            Windows:
            venv\Scripts\activate

            macOS/Linux:
            source venv/bin/activate

## Install Dependencies
    Install all required Python packages using requirements.txt:
    pip install -r requirements.txt

## Set Up Environment Variables
    Create a .env file in the root directory of the project and add the following environment variables:

makefile

FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=2b7697b98a3fe9dfbe3365ecb10e000a
FLASK_DEBUG=0
SQLALCHEMY_DATABASE_URI=postgresql://alwglass:l7Q54KORzemCBYlGiJ0gh4ddGFnTT2eb@dpg-crphhlqj1k6c73c68hag-a.oregon-postgres.render.com/portfolio_db_xvin

![alt text](./app/static/secrets.png)

## Initialize the Application
You may need to initialize some data or perform migrations (if applicable). If not, you can skip this step.

If the application is in first time use of setting up on a temp SQLLite the static data tables can be updated with provided ".py"
This will check if The database has the required static data For the dropdown inputs, if not the query will insert To the tables

![alt text](./app/static/insert_py_files.png)

## DB Entries Can be checked in DBMS

### PGAdmin
![alt text](./app/static/PGAdmin.png)

### SQLLite -  Back Up for DEMO
![alt text](./app/static/SQLLite_DB_Browser.png.png)


### Sample Queries
select * from portfolio_assets;
select * from asset_history order by asset_id, date desc;
select * from user_details;
select * from portfolio;
select * from assets;
select * from role;
select * from user_roles;



### Run the Application
Start the Flask development server:

bash

flask run
Open your browser and go to http://127.0.0.1:5000 to access the application.

Application Structure
app.py: The main Flask application file containing route definitions.
templates/: HTML templates for rendering web pages.
static/: Static files such as CSS, JavaScript, and images.
requirements.txt: A list of all dependencies needed to run the application.
.env: Environment variables for configuration (should be created manually). Included in Zip file
Key Routes
/: Home page or landing page.
/login: User login page.
/dashboard_1: User's portfolio dashboard.
/add_stock: Add a new stock to the portfolio (POST only).
/remove_stock/<string:stock_code>: Remove a stock from the portfolio.
Debugging

# Features of Dashboard

![alt text](./app/static/dashboard.png)

## Y! -  Refresh Toggle
 Turns on and off the fetch yahoo prices for The stocks in the portfolio
 This toggle is controlled tith the Y! -  Refresh switch on the Dashboard(e.g., when adding stocks or using Search).
    If this is set To ON the Application Will refresh all prices in the Portfolio when a new Stock is added
    Alternatively you can leave it  off  - if an svg file has previoulsy been created it will show the data as of created date.
 Turn on to retrieve Data to create the svg to show stock performance etc.

## Stock Symbol - OnCLick
 Once Data is refreshed from Yahoo -  this Will save the to the database while creating a svg xml  (also Saves this to the database for future retieval)

![alt text](./app/static/svg_example.png)

## Add Stocks

### Select stock from Dropdown  -  
    When selected the the buy Price Field will get the latest price from Yahoo Finance
    Enter the Comment
    Enter The amount of stocks to buy

### Click Buy
    Will Add the stock To the select portfolio
    Reduce the amount of capital (volume * buy price)

### Click Sell
    Will add the amount back to the capital of the portfolio (volume * sell price)
    Reduce the number of shares of that asset in the portfolio
        If Ticker not in port folio  -  respond with flash
        If Ticker is in portfolio but input volume > volume in portfolio the n respond

### Click Refresh
    Updates the Buy sell price from Yahoo

 ![alt text](./app/static/buy_sell_refresh.png)


# Portfolio UI

## Fuctionality 

![alt text](./app/static/portfolios.png)

### Create portfolio - 
    Add a Portfolio anem  and amount of capiltal you want To begin with

### Portfolio Overview
Select single portfolio or "All" from dropdown and click Refresh
This will Show all portfolios with a "Details" toggle to expand each row in Accordian to show further details




