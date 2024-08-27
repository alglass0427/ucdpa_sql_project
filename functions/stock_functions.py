import os
import json
import yfinance as yf
import matplotlib.pyplot as plt
import tempfile
import datetime


CURRENT_DIR =  os.getcwd()
USER_DIRECTORY =  'user_directory.json'
PERSISTENT_DIR =  os.path.join(CURRENT_DIR, 'persistent')
USER_DATA_FOLDER = os.path.join(PERSISTENT_DIR, 'users')
ACCOUNTS_FILE = os.path.join(PERSISTENT_DIR, 'accounts', 'accounts.json')


# Function to get stock price using Yahoo Finance API
def get_stock_price(stock_code,yf_flag,user_id,buy_price):
    # print(yf_flag)
    if yf_flag == 'on':
        try:
            # ------------------------------------------------------------------------
            # stock = yf.Ticker(stock_code)
            # print(f"{stock.isin}")
            # # stock.news
            # stock_info = stock.history(period="1mo")  # Get the latest day of trading data
            # print(f"{stock_info} :  Is the data")
            # -------------------------------------------------------------------------
            # Fetch stock data
            # stock_code = 'AAPL'  # Example: Apple stock
            # stock_code = 'AAPL'  # Example: Apple stock
# Assuming your Flask app has a static directory
            path = os.getcwd()
            # parent_folder  =  os.path.abspath(os.path.join(path, os.pardir))

            static_folder  = os.path.join(path, f"app/static/graphs/{user_id}")
            if not os.path.exists(static_folder):
                print(f"Creating user data folder at {static_folder}")
                os.makedirs(static_folder)

            # static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
            svg_filename = f"{stock_code}_performance.svg"
            svg_file_path = os.path.join(static_folder, svg_filename)

            # Fetch stock data

            stock = yf.Ticker(stock_code)

            # Get historical data for the past month
            stock_info = stock.history(period="1mo")

            # Input buy price (manually specified)
            buy_price = buy_price  # Example: You bought the stock at $150

            # Calculate the moving average (optional)
            stock_info['7 Day MA'] = stock_info['Close'].rolling(window=7).mean()

            # Create a plot
            plt.figure(figsize=(10, 5))

            # Plot the closing price
            plt.plot(stock_info.index, stock_info['Close'], label='Closing Price', color='blue')

            # Plot the 20-day moving average
            plt.plot(stock_info.index, stock_info['7 Day MA'], label='7 Day MA', color='orange')

            # Plot the buy price as a horizontal benchmark line
            plt.axhline(y=buy_price, color='green', linestyle='--', label=f'Buy Price (${buy_price})')
            today = datetime.date.today()
            
            # Add labels and title
            plt.title(f'{stock_code} Stock Performance - Last 1 Month - As of {today}')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.legend()

            # Save the plot to the static directory as an SVG
            plt.savefig(svg_file_path, format='svg')

            # Close the plot
            plt.close()

            print(f"SVG file saved at: {svg_file_path}")


            if not stock_info.empty:
                print(f"Returned to dashboard : {stock_code},{round(stock_info['Close'].iloc[-1], 2)},{stock.isin}")
                return (stock_code,round(stock_info['Close'].iloc[-1], 2),stock.isin)  # Get the last closing price
            else:
                return (("Invalid Ticker","",""))
        except Exception as e:
            return "Error: " + str(e)
    # Test Response
    else:
        return ("","","")
# def get_all_prices ():
#     stocks_with_prices = [(stock, get_stock_price(stock)) for stock in user_data['portfolio']]

# Load the user's portfolio from their JSON file
def load_user_portfolio(username):
    
    user_file_path = os.path.join(USER_DATA_FOLDER, f"{username}.json")
    print(user_file_path)
    if os.path.exists(user_file_path):
        with open(user_file_path, 'r') as f:
            print(f)
            return json.load(f)
            
    # return {"username": username, "portfolio": []}
    return {}

# Save the user's portfolio to their JSON file
def save_user_portfolio(username, portfolio):
    user_file_path = os.path.join(USER_DATA_FOLDER, f"{username}.json")
    print(f"Save User File Path : {user_file_path}")
    with open(user_file_path, 'w') as f:
        print(f" save user portfolio function : stocks are , {f} ")
        # json.dump({"username": username, "portfolio": portfolio}, f)
        json.dump(portfolio, f)


# Load all user accounts from the JSON file
def load_user_accounts():
    with open(ACCOUNTS_FILE, 'r') as f:
        print(f" INSIDE load user accounts function : accounts are , {f} ")
        
        return json.load(f)

# Save user accounts to the JSON file
def save_user_accounts(accounts):
    with open(ACCOUNTS_FILE, 'w') as f:
        
        json.dump(accounts, f)