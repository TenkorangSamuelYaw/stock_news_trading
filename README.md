# stock_news_trading
This project is a DIY Bloomberg Terminal.
The Bloomberg Terminal is a computer software system that provides financial professionals with real-time financial data, news feeds, messaging, and trading capabilities.
It is a subscription-based service that is widely used by financial institutions, investment banks, and other organizations involved in the financial industry
The bloomberg terminal's annual subscription is $24,000.00
The goal of this project is to create a poor man's bloomberg terminal for upcoming stock traders to help them with their stock trading.
Using the request module in python, an API call is made to the daily api (https://www.alphavantage.co/documentation/#daily)
This API returns raw (as-traded) daily time series (date, daily open, daily high, daily low, daily close, daily volume) of the global equity specified, covering 20+ years of historical data.
With the help of https://jsonviewer.stack.hu/, the json data is nicely viewed, and relevant data is retrieved.
Yesterday's closing stock price and the day before yesterday's closing stock price is retrieved.
The positive difference is worked out using the abs() function, and the percentage difference in price between closing price yesterday and closing price the day before yesterday is calculated.
If the percentage is greater than 5 then the News API is used to get articles related to the company name.
Each article is sent as a separate message via Twilio to the user.
