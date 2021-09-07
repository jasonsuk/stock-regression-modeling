'''
Saving S&P500 tickers and load stock information from Yahoo Finance
Inspired by a Real Python post on https://pythonprogramming.net/sp500-company-price-data-python-programming-for-finance/
'''


from bs4 import BeautifulSoup
import requests
import os
import pickle
import yfinance as yf
import pandas as pd
import numpy as np

# Get A list of S&P 500 tickers from a Wikipedia page
sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'


def get_sp500_tickers(url=sp500_url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)  # Exit with error message

    table = soup.find('table', {'class': 'wikitable'})
    rows = table.find_all('tr')[1:]  # row data for details of each company
    tickers = []
    tickers_meta = []
    for row in rows:
        data = row.find_all('td')
        tickers.append(data[0].text.strip())
        tickers_meta.append({
            'Ticker': data[0].text.strip(),
            'Security': data[1].text.strip(),
            'Sector': data[3].text.strip(),
            'Sub_industry': data[4].text.strip(),
            'Headquarter_location': data[5].text.strip(),
            'Date_first_added': data[6].text.strip(),
            'CIK': data[7].text.strip(),
            'Founded': data[8].text.strip()

        })

    # Save the tickers in a pickle file so it does not load all the time
    pickle.dump(tickers, open('data/sp500.p', 'wb'))

    # Create meta data to contain company details
    meta = pd.DataFrame.from_dict(tickers_meta)
    meta.to_csv('data/company_meta.csv', index=False)


def get_yahoo_stock_data(reload_sp500_data=False):

    if reload_sp500_data:
        tickers = get_sp500_companies()
    else:
        tickers = pickle.load(open('data/sp500.p', 'rb'))

    # Get stock data with rearranged tickers
    tickers = ' '.join(tickers)
    data = yf.download(tickers=tickers, period='max', interval='1d')

    # Save data
    data['Adj Close'].to_csv('data/adj_prices.csv')
    data['Close'].to_csv('data/prices.csv')
    data['Volume'].to_csv('data/volumes.csv')


if __name__ == '__main__':
    # Run only once to save the stock data
    get_yahoo_stock_data()


'''
2 Failed downloads:
- BF.B: 1d data not available for startTime=-2208988800 and endTime=1630245075. Only 100 years worth of day granularity data are allowed to be fetched per request.
- BRK.B: No data found, symbol may be delisted
'''
