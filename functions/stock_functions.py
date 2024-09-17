import os
import json
import yfinance as yf
import matplotlib.pyplot as plt
import tempfile
from datetime import datetime, timedelta, date
from app.models import Asset , AssetHistory , PortfolioAsset ,  Portfolio
from app import db
import io
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend
import matplotlib.pyplot as plt
from sqlalchemy import func

import pandas as pd
from yahooquery import Ticker
from concurrent.futures import ThreadPoolExecutor
CURRENT_DIR =  os.getcwd()


###################################################################################
####GET SINGLE LATEST PRICE
###################################################################################
def get_latest_price (ticker):
    stock = yf.Ticker(ticker)
    stock_info = stock.history(period="1d", actions=False,rounding=True)
    print(stock_info)
    last_quote = stock_info['Close'].iloc[-1]
    print (f" Last Quote : {last_quote}")
    return last_quote

###################################################################################
####GET LATEST PRICES FROM A LIST OF ASSETS IN THE PORTFOLIO
###################################################################################

def get_latest_portfolio_prices(portfolio):
    print(portfolio)
    # Query your database for the tickers in the portfolio (assuming a PortfolioAsset model)
    portfolio_assets = db.session.query(PortfolioAsset, Asset).\
        join(Asset, PortfolioAsset.asset_id == Asset.id).\
        filter(PortfolioAsset.portfolio_id == portfolio).all()
    print(portfolio_assets)
    # Extract tickers from the portfolio assets
    tickers = [asset.ticker for portfolio_asset, asset in portfolio_assets if asset.ticker != "CASH"]
    if not tickers:
        # If no tickers are provided, return an empty dictionary or handle accordingly
        print("No stocks available in the portfolio.")
        return {}

    # Fetch the latest stock prices from Yahoo Finance
    ticker_data = yf.download(tickers, period="1d", interval="1d" ,actions=False,rounding=True)
    closing_prices = ticker_data['Close'].iloc[-1]  # Get the last available row (latest data)

        # Check if the result contains multiple tickers or just one
    if len(tickers) == 1:
        # If there's only one ticker, yfinance returns a scalar DataFrame
        closing_prices = ticker_data['Close']
        return {tickers[0]: closing_prices.iloc[-1]}  # Single ticker case
    else:
        # If multiple tickers, fetch the closing prices as a Series
        closing_prices = ticker_data['Close'].iloc[-1]  # Last available row
        return {ticker: closing_prices[ticker] for ticker in tickers}

###################################################################################
####GET MAX DATE FOR ASSET IN TO REDUCE REQUEST DATE RANGE
###################################################################################

def get_max_date_for_asset(asset_id):
    max_date = db.session.query(func.max(AssetHistory.date)).filter_by(asset_id=asset_id).scalar()
    return max_date   

###################################################################################
####REQUEST PRICES FOR MAX 30 DAYS FROM YAHOO
################################################################################### 
# Function to get stock price using Yahoo Finance API
def get_stock_price(stock_code,asset_id,portfolio,yf_flag,user_id,buy_price):
    # print(yf_flag)
    print(f"Stock Code {stock_code}")
    print(f"Asset ID {asset_id}")
    print(f"Portfolio ID {portfolio}")
    print(f"yf_flag {yf_flag}")
    print(f"user_id {user_id}")
    print(f"buy_price {buy_price}")
    if yf_flag == 'on' and stock_code != "CASH":
 
        try:
            max_date = get_max_date_for_asset(asset_id)
            if max_date is None:
                print(f"Max Date NONE : {max_date}")
                start_date = datetime.today() - timedelta(days=30)  # Default to 1 month ago if no data
            else:
                print(f"Max Date : {max_date}")
                start_date = max_date  # Next day after max date
            
            end_date = datetime.today()
            ##create an object of the yahoo ticker
            stock = yf.Ticker(stock_code)
            ##get the history from 30 days max  - max date to today or 30 days to create the graph
            yahoo_stock_info = stock.history(start=start_date, end=end_date, actions=False, rounding=True)
       
            yahoo_stock_info.dropna(inplace=True)
            # Fetch historical data using yfinance

            # Insert or update the historical data into the database
            #REASON - - -- - IF YAHOO FLAG IS OFF THE SVG CAN STILL BE CREATED
            for date, row in yahoo_stock_info.iterrows():
                date_only = date.date()  # Get only the date part (without time)
                
                # Check if the record already exists
                existing_entry = AssetHistory.query.filter_by(asset_id=asset_id, date=date_only).first()
                
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
                        asset_id=asset_id,
                        date=date_only,
                        open_price=row['Open'],
                        high_price=row['High'],
                        low_price=row['Low'],
                        close_price=row['Close'],
                        volume=row['Volume']
                    )
                    db.session.add(history_entry)
          ##INSERT TO DB  
            db.session.commit()
            print(f"Historical data for {stock_code} saved/updated successfully.")

            ################exit yahoo try
        except Exception as e:
            print(f"Error processing yahoo DATA {stock_code}: {e}")
            return "Error: " + str(e)
        
        ######END IF yf_flag is Y - - -  add Condition to based on MAX Date 

        # Input buy price (manually specified)
        # buy_price = buy_price  # Example: You bought the stock at $150
    print(f"THIS IS THE BUY PRICE IN STOCK FUNCTION  ::::::  {buy_price}")
    
    today = datetime.today()
    ##############DATABASE PRICES INSTEAD OF YFINANCE DIRECT  ####################################  
    
    # Query the AssetHistory table for the asset's historical data  -  USE THE ASSET HISTORY RELATIONSHIP TO THE PORTFOLIO ASSET
    # PRICES ARE AGNOSTIC OF PORTFOLIO THAT HOLDS THE ASSET
    historical_data = db.session.query(AssetHistory).filter(
        AssetHistory.asset_id == asset_id,   ###AssetHistory id  =  Asset it relationship on PK
        AssetHistory.date >= today - timedelta(days=30)  # Get data for the last 30 days
    ).order_by(AssetHistory.date).all()

    print(historical_data)
    # Prepare lists for plotting
    dates = [entry.date for entry in historical_data]
    closing_prices = [entry.close_price for entry in historical_data]

    ####USE PANDAS To creeate the data frams
    stock_info = pd.DataFrame({
                                'Date': dates,
                                'Close': closing_prices
                            })
    stock_info.set_index('Date', inplace=True)
    if len(closing_prices) >= 7:
        
        moving_averages = [
        sum(closing_prices[i-7:i]) / 7 if i >= 7 else None for i in range(len(closing_prices))
        ]
        stock_info['SMA'] = stock_info['Close'].rolling(window=7).mean().dropna()  ##mean
        stock_info['STD'] = stock_info['Close'].rolling(window=7).std().dropna()   ##standard deviation
        print(stock_info.head())
        print(stock_info.dtypes)
        # Calculate the Upper and Lower Bollinger Bands
        stock_info['Upper Band'] = stock_info['SMA'] + (stock_info['STD'] * 1.96)
        stock_info['Lower Band'] = stock_info['SMA'] - (stock_info['STD'] * 1.96)


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


    ########SVG FROM DATABASE #########
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
    # portfolio = Portfolio.query.filter_by(user_id=user_id).first()

    # Check if the portfolio exists
    if portfolio:
        print(f"Portfolio ID: {portfolio}")

        # Fetch the PortfolioAsset instance
        # portfolio_asset = PortfolioAsset.query.filter_by(portfolio_id=portfolio.id, asset_id=asset.id).first()
        portfolio_asset = PortfolioAsset.query.filter_by(portfolio_id=portfolio, asset_id=asset_id).first()
        
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
            print(f"No Portfolio Asset found for Portfolio ID: {portfolio.id} and Asset ID: {asset_id}")
    else:
        print(f"No Portfolio found for User ID: {user_id}")

    if not stock_info.empty:
        print(f"Returned to dashboard : {stock_code},{round(stock_info['Close'].iloc[-1], 2)},{stock.isin}")
        return (stock_code,round(stock_info['Close'].iloc[-1], 2),stock.isin)  # Get the last closing price
    else:
        return (("Invalid Ticker","",""))
    
# Test Response
# else:
#     return ("","","")
# def get_all_prices ():
#     stocks_with_prices = [(stock, get_stock_price(stock)) for stock in user_data['portfolio']]
