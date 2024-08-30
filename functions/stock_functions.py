import os
import json
import yfinance as yf
import matplotlib.pyplot as plt
import tempfile
from datetime import datetime, timedelta
from app.models import Asset , AssetHistory , PortfolioAsset ,  Portfolio
from app import db
import io
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend
import matplotlib.pyplot as plt
import pandas as pd

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

            # print(stock)
            # Get historical data for the past month
            stock_info = stock.history(period="1mo")
            stock_info['SMA'] = stock_info['Close'].rolling(window=20).mean()  ##mean
            stock_info['STD'] = stock_info['Close'].rolling(window=20).std()   ##standard deviation

            # Calculate the Upper and Lower Bollinger Bands
            stock_info['Upper Band'] = stock_info['SMA'] + (stock_info['STD'] * 1.96)
            stock_info['Lower Band'] = stock_info['SMA'] - (stock_info['STD'] * 1.96)

            # Fetch historical data using yfinance

            asset = Asset.query.filter_by(ticker=stock_code).first()  #######TO MANY DB CALLS
            if not asset:
                print(f"No asset found with ticker {stock_code}")
                return

            # Insert or update the historical data into the database
            for date, row in stock_info.iterrows():
                date_only = date.date()  # Get only the date part (without time)
                
                # Check if the record already exists
                existing_entry = AssetHistory.query.filter_by(asset_id=asset.id, date=date_only).first()
                
                if existing_entry:
                    # Update the existing record
                    existing_entry.open_price = row['Open']
                    existing_entry.high_price = row['High']
                    existing_entry.low_price = row['Low']
                    existing_entry.close_price = row['Close']
                    existing_entry.volume = row['Volume']
                else:
                    # Create a new record
                    history_entry = AssetHistory(
                        asset_id=asset.id,
                        date=date_only,
                        open_price=row['Open'],
                        high_price=row['High'],
                        low_price=row['Low'],
                        close_price=row['Close'],
                        volume=row['Volume']
                    )
                    db.session.add(history_entry)
            
            db.session.commit()
            print(f"Historical data for {stock_code} saved/updated successfully.")


            # Input buy price (manually specified)
            # buy_price = buy_price  # Example: You bought the stock at $150
            print(f"THIS IS THE BUY PRICE IN STOCK FUNCTION  ::::::  {buy_price}")
            
            today = datetime.today()

            # Query the AssetHistory table for the asset's historical data
            historical_data = db.session.query(AssetHistory).filter(
                AssetHistory.asset_id == asset.id,   ###AssetHistory id  =  Asset it relationship on PK
                AssetHistory.date >= today - timedelta(days=30)  # Get data for the last 30 days
            ).order_by(AssetHistory.date).all()

            print(historical_data)
            # Prepare lists for plotting
            dates = [entry.date for entry in historical_data]
            closing_prices = [entry.close_price for entry in historical_data]
            moving_averages = [entry.close_price for entry in historical_data]  # Replace this with actual MA logic if necessary

            # Calculate the 7-day moving average
            if len(closing_prices) >= 7:
                moving_averages = [
                    sum(closing_prices[i-7:i]) / 7 if i >= 7 else None for i in range(len(closing_prices))
                ]

    #########################EXAMPLE OF LONG FORM ####################################
    # Initialize an empty list to hold the 7-day moving averages
            # moving_averages = []

            # # Iterate over the list of closing prices by index
            # for i in range(len(closing_prices)):
                
            #     # Check if the current index is at least 7 (i.e., there are enough previous prices to calculate a 7-day average)
            #     if i >= 7:
            #         # Calculate the sum of the last 7 prices
            #         last_seven_sum = 0
            #         for j in range(i-7, i):
            #             last_seven_sum += closing_prices[j]
                    
            #         # Calculate the average by dividing the sum by 7
            #         moving_average = last_seven_sum / 7
                    
            #         # Append the calculated moving average to the list
            #         moving_averages.append(moving_average)
            #     else:
            #         # If there aren't enough previous prices, append None
            #         moving_averages.append(None)

            # # At the end of this loop, moving_averages will contain the 7-day moving average values
            # # with None for the first 6 indices


            else:
                moving_averages = [None] * len(closing_prices)  # Not enough data for MA
            print(f"Moving Averages : {moving_averages}")
            # # Create a plot
            # plt.figure(figsize=(10, 5))

            # # Plot the closing price
            # plt.plot(dates, closing_prices, label='Closing Price', color='blue')

            # # Plot the 7-day moving average
            # plt.plot(dates, moving_averages, label='7 Day MA', color='orange')

            # # Plot the buy price as a horizontal benchmark line
            # plt.axhline(y=buy_price, color='green', linestyle='--', label=f'Buy Price (${buy_price})')

            # # Add labels and title
            # plt.title(f'{stock_code} Stock Performance - Last 1 Month - As of {today.date()}')
            # plt.xlabel('Date')
            # plt.ylabel('Price')
            # plt.legend()

            # # Save the plot to the static directory as an SVG
            # plt.savefig(svg_file_path, format='svg')

            # # Close the plot
            # plt.close()
    


########SVG #########
            # Prepare to capture SVG output
            svg_buffer = io.StringIO()

            # Create a plot
            plt.figure(figsize=(10, 5))

            # Plot the closing price
            plt.plot(dates, closing_prices, label='Closing Price', color='blue')

            # Plot Upper
            plt.plot(stock_info.index, stock_info['Upper Band'], label='Upper Band', color='green')

            # Plot the 7-day moving average
            plt.plot(dates, moving_averages, label='7 Day MA', color='orange')
            
            plt.plot(stock_info.index, stock_info['Lower Band'], label='Lower Band', color='red')

            plt.fill_between(stock_info.index, stock_info['Lower Band'], stock_info['Upper Band'], color='gray', alpha=0.3)
             
            # Plot the buy price as a horizontal benchmark line
            plt.axhline(y=buy_price, color='green', linestyle='--', label=f'Buy Price (${buy_price})')
            

            # Add labels and title
            plt.title(f'{stock_code} Stock Performance - Last 1 Month - As of {today.date()}')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.legend()

            # Save the plot to the SVG buffer
            plt.savefig(svg_buffer, format='svg')
            plt.close()  # Close the plot to free up memory

# Get the SVG content as a string
            svg_content = svg_buffer.getvalue()
            svg_buffer.close()  # Close the buffer

            # Fetch the portfolio based on user_id
            portfolio = Portfolio.query.filter_by(user_id=user_id).first()

            # Check if the portfolio exists
            if portfolio:
                print(f"Portfolio ID: {portfolio.id}")

                # Fetch the PortfolioAsset instance
                portfolio_asset = PortfolioAsset.query.filter_by(portfolio_id=portfolio.id, asset_id=asset.id).first()
                
                if portfolio_asset:
                    print(f"Found Portfolio Asset: {portfolio_asset}")

                    # Update the svg_content
                    portfolio_asset.svg_content = svg_content
                    print(f"Updated Portfolio Asset: {portfolio_asset}")

                    # Commit the changes to the database
                    try:
                        db.session.commit()
                        print("SVG content updated successfully.")
                    except Exception as e:
                        db.session.rollback()  # Rollback in case of error
                        print(f"Error committing changes: {e}")
                else:
                    print(f"No Portfolio Asset found for Portfolio ID: {portfolio.id} and Asset ID: {asset.id}")
            else:
                print(f"No Portfolio found for User ID: {user_id}")

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