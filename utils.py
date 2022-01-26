import datetime as dt
from yahoo_fin import stock_info
import yfinance as yf

def get_company_name(selected_ticker):
    company = yf.Ticker(selected_ticker)
    return company.info['longName']

def get_today():
    return dt.datetime.today()
# Function that sets start_date based on timespan selected 
def set_timespan(timespan=30):
    today = get_today()
    delta_days = 30

    if timespan =="3M":
        delta_days = 90
    elif timespan == "6M":
        delta_days = 180
    elif timespan == "YTD":
        curr_year = today.year
        delta_days = (today.date() - dt.date(curr_year,1,1)).days
    elif timespan == "1Y":
        delta_days = 365
    elif timespan == "3Y":
        delta_days = 365*3
    elif timespan == "5Y":
        delta_days = 365*5
    elif timespan == "MAX":
        delta_days = 365*100
    else:
        delta_days = timespan
    
    delta = dt.timedelta(days=delta_days)
    return (today.now() - delta).strftime('%m/%d/%Y')

def get_stock_data(ticker, start, end, interval = "1d"):
    return stock_info.get_data(ticker, start_date=start, end_date=end, interval=interval)

def get_company_info(ticker):
    return stock_info.get_company_info(ticker)

def is_numeric(val):
    try:
        float(val)
        return True
    except ValueError:
        return False