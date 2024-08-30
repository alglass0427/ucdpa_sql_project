from app_test import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)



               # candle = go.Candlestick(x=df.index, open = df['Open'], high = df['High'], low = df['Low'], close = df['Close'], name = 'Candlestick')
            # closing_prices = [entry.close_price for entry in historical_data]
                        



            # upper_line = go.Scatter(x = stock_info.index, y = stock_info['Upper Band'], line = dict(color = 'rgba(250, 0, 0, 0.75)', width = 1), name = 'Upper Band')
    
            # middle_line = go.Scatter(x = stock_info.index, y = stock_info['Middle Band'], line = dict(color = 'rgba(0, 0, 250, 0.75)', width = 1), name = 'Middle Band')
    
            # lower_line = go.Scatter(x = stock_info.index, y = stock_info['Lower Band'], line = dict(color = 'rgba(0, 250, 0, 0.75)', width = 1), name = 'Lower Band')

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