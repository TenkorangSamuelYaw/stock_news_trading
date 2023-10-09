import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API = "RYXT5XC04T9BXEAO"
NEWS_API = "377dce95b7c641589895eae453c6daeb"
TWILIO_SID = "AC3479619d1fb985b0368c430aa6146ed9"
TWILIO_AUTH_TOKEN = "184ef2e3c733f5b2b1bbbbb535df37d0"

# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API,
}
stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]  # The Meta Data key is not required.
stock_data_list = [value for (key, value) in stock_data.items()]

#  Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries.
#  e.g. [new_value for (key, value) in dictionary.items()]
yesterday_data = stock_data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

#  Get the day before yesterday's closing stock price
day_before_yesterday_data = stock_data_list[10]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

#  Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
#  Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down: str
if difference > 0:
    #  In this case positive
    up_down = "🔺"
else:
    up_down = "🔻"
#  Work out the percentage difference in price between closing price yesterday & closing price the day before yesterday
percentage_difference = (difference / float(yesterday_closing_price) * 100)

#  If TODO4 percentage is greater than 5 then print("Get News").
if abs(percentage_difference) > 5:
    # STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    #  Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API,
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_articles = news_response.json()["articles"]
    #  Use Python slice operator to create a list that contains the first 3 articles.
    #  Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = news_articles[:3]  # Get first 3 articles.
    print(three_articles)

    # STEP 3: Use twilio.com/docs/sms/quickstart/python
    #  to send a separate message with each article's title and description to your phone number.

#  Create a new list of the first 3 article's headline and description using list comprehension.
formatted_articles = [f"{STOCK_NAME}: {up_down}%\n:Headline: {article['title']}. \nBrief: {article['description']}"
                      for article in three_articles]
print(formatted_articles)
#  Send each article as a separate message via Twilio.
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
for f_article in formatted_articles:
    message = client.messages \
        .create(
        body=f_article,
        from_="+12564879574",
        to="+233204676251"
    )
    print(message.status)

# Optional Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
