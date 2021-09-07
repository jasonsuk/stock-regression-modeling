
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

assets = pd.read_csv('data/final_asset_data.csv')

# Get ticker options for allocation input
ticker_options = []

for ticker in assets.columns:
    ticker_dict = dict()
    ticker_dict['label'] = ticker
    ticker_dict['value'] = ticker
    ticker_options.append(ticker_dict)


# Input/interactive components


allocation_input = dbc.FormGroup(
    className='allocation-input',
    children=[
        html.Div(
            className='chart-header',
            children=[
                html.H3('Display a portfolio allocation'),
                html.P('Select the assets of your interest'),
            ]
        ),
        dcc.Dropdown(
            id='ticker-symbols',
            className='dropdown-allocation',
            options=ticker_options,
            value=['AAPL', 'MSFT', 'IBM', 'GOOGL'],
            multi=True
        ),
        dbc.Button(id='button-allocation',
                   className='button button-allocation',
                   children='Display the suggested asset allocation',
                   color="secondary",
                   block=True)
    ]
)


charts = html.Div(
    children=[
        html.Div(
            children=dcc.Graph(
                id='chart-allocation',
                className='chart chart-allocation',
                config={'displayModeBar': False},
            )
        ),
        html.Div(
            children=dcc.Graph(
                id='chart-performance',
                className='chart chart-performance',
                config={'displayModeBar': False},
            )
        )
    ]

)
