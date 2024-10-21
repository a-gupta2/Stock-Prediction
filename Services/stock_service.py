import pandas as pd
import requests
from io import StringIO
import yfinance as yf


def get_sp500_stocks(url):
    response = requests.get(url)
    html_content = response.text
    data = pd.read_html(StringIO(html_content))[0]
    return data[['Symbol', 'Security']]


def get_stock_fundamentals(stock_name):
    stock = yf.Ticker(stock_name)
    fundamentals = {
        'PE Ratio (TTM)': stock.info.get('forwardPE', 'N/A'),
        'Market Cap': stock.info.get('marketCap', 'N/A'),
        'Dividend Yield': stock.info.get('dividendYield', 'N/A'),
        'EPS (TTM)': stock.info.get('trailingEps', 'N/A'),
        'Revenue': stock.info.get('totalRevenue', 'N/A'),
        'Profit Margin': stock.info.get('profitMargins', 'N/A'),
    }
    return fundamentals


def get_stock_data_from_yf(stock_name, start_date='1996-01-01'):
    stock_data = yf.download(stock_name, start=start_date, progress=False)
    stock_data.reset_index(inplace=True)
    return stock_data
