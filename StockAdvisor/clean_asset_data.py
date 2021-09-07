import pandas as pd

# Function to get price data of S&P500 stocks


def get_asset_data():
    assets = pd.read_csv('data/prices.csv', index_col=0)
    total_tickers = len(assets.columns)
    # print('Total number of companies: %s' % total_tickers)
    return assets

# Function to clean stock data


def final_asset_data(start_since):
    assets = get_asset_data()

    # Dealing with the historic price information from 2000 onwards
    print(f'Subsetting data to range from {start_since}')
    assets = assets.loc[start_since:].copy()

    # Dealing with missing values
    null_info = assets.isnull().mean(axis=0).sort_values(ascending=False)
    drop_list = list(null_info[null_info > 0.3].index)
    assets = assets.drop(columns=drop_list)
    print('Deleted asset ticker(s) that have more than 30% missing data\n',
          'Now dealing with {} tickers'.format(len(assets.columns)))

    # Fill missing values with interpolation
    # As it is time series with a quite narros interval (every business data)
    # interpolating (forward with the last value available) makes sense
    assets = assets.fillna(method='ffill')

    # There are still some tickers with missing values
    # keep them for a while and let's visualize it first

    final_null = assets.isnull().any().sum()
    print('Stock prices have been forward filled\n',
          'There still are {} tickers that have missing values'.format(int(assets.isnull().any().sum())))

    assets.to_csv('data/final_asset_data.csv', index=True)
    print('Cleaned final data has been saved in "data/final_asset_data.csv"')


# Save the clean data
# Starting from 2015

final_asset_data('2015-01-01')
