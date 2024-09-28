# ucdpa_sql_project

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
    git clone https://github.com/alglass0427/ucdpa_sql_project.git`

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

 

app/__init.py: The main Flask application file containing route definitions.
models.py: - Database Table structure
run.py: runs the programme
routes.py - stores The routes And Functions
templates/: HTML templates for rendering web pages.
static/: Static files such as CSS, JavaScript, and images.
functions/: functions to import
requirements.txt: A list of all dependencies needed to run the application.
.env: Environment variables for configuration (should be created manually). Included in Zip file
Key Routes
/: Home page or landing page.
/login: User login page.
/dashboard_2: User's portfolio dashboard.
/portfolio: User's portfolio info.
/add_portfolio :  add user portfolio
/add_stock: Add a new stock to the portfolio (POST only).
/remove_stock/<string:stock_code>: Remove a stock from the portfolio.
Debugging

# Points to Note
## SQL

Use of CTE in Portfolio Aggregate Queries

A Common Table Expression (CTE) in SQL is a temporary result set that you can define within a query using the WITH clause. It exists only for the duration of that query and is used to simplify complex queries by breaking them into more readable parts. CTEs are particularly useful when you need to write recursive queries or perform multi-step operations. A CTE can be referenced multiple times within the main query, which makes it easier to manage and maintain code, especially in complex joins, subqueries, or aggregations.

One of the key benefits of CTEs is improved readability and organization. Instead of nesting subqueries, which can make the code difficult to follow, CTEs allow developers to structure their queries in a logical, step-by-step manner. Additionally, CTEs can improve performance by reducing redundant code, especially when the same complex subquery needs to be used multiple times in a query. Recursive CTEs, in particular, enable handling hierarchical or tree-structured data more efficiently, such as organizational charts or category hierarchies.

### CTE

![alt text](./app/static/CTE.png)

### ERD

![alt text](./app/static/ERD.png)

## JAVA use fetch to add / remove update the Database
Fetch The response of of the Routed HTMLS file and then udate the portion of  the table to prevent full page refresh in full render_template

## HTML 

Use of templates to updaate portions of the web pages 

Dashboard_tbl.html
Portfolio_rows.html

### Example 

![alt text](./app/static/fetch.png)