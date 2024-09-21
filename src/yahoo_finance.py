import yfinance as yf

def get_yahoo_data(ticker, start_date, end_date):
  data = yf.download(ticker, start=start_date, end=end_date)
  return data

def get_action_name(ticker):
  stock = yf.Ticker(ticker)
  return stock.info['shortName']
