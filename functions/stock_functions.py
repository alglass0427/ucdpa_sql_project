import os
import json
import yfinance as yf

CURRENT_DIR =  os.getcwd()
USER_DIRECTORY =  'user_directory.json'
PERSISTENT_DIR =  os.path.join(CURRENT_DIR, 'persistent')
USER_DATA_FOLDER = os.path.join(PERSISTENT_DIR, 'users')
ACCOUNTS_FILE = os.path.join(PERSISTENT_DIR, 'accounts', 'accounts.json')


# Function to get stock price using Yahoo Finance API
def get_stock_price(stock_code,yf_flag):
    # print(yf_flag)
    if yf_flag == 'on':
        try:
            stock = yf.Ticker(stock_code)
            print(f"{stock.isin}")
            # stock.news
            stock_info = stock.history(period="1d")  # Get the latest day of trading data
            print(f"{stock_info} :  Is the data")
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