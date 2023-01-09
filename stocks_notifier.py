import requests
from datetime import date, timedelta
from os import environ

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def get_stocks_data():
  ALPHA_API_KEY = "LUJU8NOAXKJIFYVY"
  ALPHA_ENDPOINT = "https://www.alphavantage.co/query"
  ALPHA_PARAMS = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": ALPHA_API_KEY
  }

  req = requests.get(url=ALPHA_ENDPOINT, params=ALPHA_PARAMS)
  req.raise_for_status()
  alpha_data = req.json()['Time Series (Daily)']
  # print(alpha_data)
  data_list = [value for (key, value) in alpha_data.items()]
  # print(data_list)
  yda_data = data_list[0]
  dby_data = data_list[1]

  # yda_close_price = round(float(alpha_data[yesterday.strftime("%Y-%m-%d")]['4. close']), 2)
  # print(f"Close price yesterday ({yesterday}): {yda_close_price} USD")
  yda_close_price = round(float(yda_data['4. close']), 2)
  print(f"Close price yesterday: {yda_close_price} USD")
  # dby_close_price = round(float(alpha_data[day_before_yesterday.strftime("%Y-%m-%d")]['4. close']), 2)
  # print(f"Close price day before yesterday ({day_before_yesterday}): {dby_close_price} USD")
  dby_close_price = round(float(dby_data['4. close']), 2)
  print(f"Close price day before yesterday: {dby_close_price} USD")
  price_variation = round(yda_close_price - dby_close_price, 2)
  print(f"Price variation: {price_variation} USD")
  stock_variation = round(price_variation / dby_close_price * 100, 2)
  print(f"Stock variation: {stock_variation} %")
  stock_info = ''
  if stock_variation >= 5:
    stock_info = f"{STOCK}: 🔺 {stock_variation} %"
  elif stock_variation <= -5:
    stock_info = f"{STOCK}: 🔻 {stock_variation} %"
  return stock_info

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
def get_news():
  NEWS_API_KEY = "d283ef5ab39b40e5b65ae04b459b101c"
  # NEWS_ENDPOINT = "https://newsapi.org/v2/top-headlines"
  NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
  NEWS_PARAMS = {
    "q": COMPANY_NAME,
    "searchIn": "title",
    # "from": date.strftime(day_before_yesterday, "%Y-%m-%d"),
    "from": day_before_yesterday.strftime("%Y-%m-%d"),
    # "to": date.strftime(yesterday, "%Y-%m-%d"),
    "to": yesterday.strftime("%Y-%m-%d"),
    # "sortBy": "publishedAt",
    # "sortBy": "popularity",
    "sortBy": "relevancy",
    "language": "en",
    # "apiKey": NEWS_API_KEY
  }

  NEWS_HEADERS = {
    "X-Api-Key": NEWS_API_KEY
  }

  req = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMS, headers=NEWS_HEADERS) # Use headers to secure request by hiding the apiKey
  req.raise_for_status()
  # print(req.url)
  news_data = req.json()['articles']
  # print(news_data)

  # news_list = []
  # for news in news_data[:3]:
  #   news_headline = f"Headline: {news['title']}"
  #   news_brief = f"Brief: {news['description']}"
  #   news_list.append(f"\n{news_headline}\n{news_brief}\n")
  news_list = [f"\nHeadline: {news['title']}\nBrief: {news['description']}\n" for news in news_data[:3]]
  return news_list

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
def send_sms(stock_info, news=''):
  TWILIO_ACCOUNT_SID = environ.get("TWILIO_ACCOUNT_SID")
  TWILIO_AUTH_TOKEN = environ.get("TWILIO_AUTH_TOKEN")
  # TWILIO_ENDPOINT = f"https://{TWILIO_ACCOUNT_SID}:{TWILIO_AUTH_TOKEN}@api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages"
  TWILIO_ENDPOINT = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages"
  TWILIO_PHONE_NR = environ.get("TWILIO_PHONE_NR")
  DEST_PHONE_NR = environ.get("DEST_PHONE_NR")
  TWILIO_PARAMS = {
    "From": TWILIO_PHONE_NR,
    "Body": stock_info + news,
    "To": DEST_PHONE_NR
  }

  post = requests.post(url=TWILIO_ENDPOINT, data=TWILIO_PARAMS, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
  post.raise_for_status()
  # print(post.url)
  print(post)

yesterday = date.today() - timedelta(days=1)
day_before_yesterday = yesterday - timedelta(days=1)
sms_enabled = False

stock_info = get_stocks_data()
if stock_info != '':
  print("\nSMS Messages:\n")
  company_news = get_news()
  if len(company_news) > 0:
    for news in company_news:
      print(stock_info)
      print(news)
      if sms_enabled:
        send_sms(stock_info, news)
  else:
    print(stock_info)
    if sms_enabled:
      send_sms(stock_info)