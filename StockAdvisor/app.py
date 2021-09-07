#!/usr/bin/env /Users/jsuk/opt/anaconda3/envs/ml_fin/bin/python

# # Load Dash package for dashboard

from helpers.load_risktolerance import predict_risk_tolerance
from helpers.load_portfolio import get_asset_allocation
from components.chart_component import allocation_input, charts
from components.rt_output_component import risk_tolerance_output
from components.form_component import form
import pandas as pd
import numpy as np
import pickle
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import warnings
warnings.filterwarnings('ignore')


# Import components

# Configuration using Bootstrap theme
# Sandstone theme - https://bootswatch.com/sandstone/

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

# Load the model - built on random forest regressor
# This will predict an individual's risk tolerance based on inputs
model = pickle.load(open('rfmodel_risk_tolerance_predictor.sav', 'rb'))


# Instntiate asset data
assets = pd.read_csv('data/final_asset_data.csv')


# Create a container that
# includes all components

app.layout = dbc.Container(
    className='mt-4 justify-contents-around',
    children=[
        # dbc.Row(
        #     className='header',
        #     children=[
        #         html.H1('Robo Advisor', className='header-title'),
        #     ]
        # ),
        dbc.Row(
            className='body',
            children=[
                dbc.Col(
                    [
                        html.Div(
                            className='form-header',
                            children=[
                                html.H3(
                                    'Risk tolerance survey'),
                                html.P(
                                    'How much can you tolerate investment risk?'),

                            ]
                        ),
                        form
                    ],
                    width=5,
                    className='body-left'
                ),

                dbc.Col(
                    [
                        risk_tolerance_output,
                        allocation_input,
                        charts
                    ],
                    width=7,
                    className='body-right'
                )
            ]
        )

    ]
)

# Callback functions


@app.callback(
    [
        # Output as a calculated risk tolerance rate
        # Which will be automatically linked as an input for asset allocation
        Output('risk-tolerance-input', 'value')
    ],
    [
        # Inputs - 1 button + 9 features
        Input('button-risktolerance', 'n_clicks'),
        Input('age-input', 'value'),
        Input('education-input', 'value'),
        Input('married-input', 'value'),
        Input('kids-input', 'value'),
        Input('occupation-input', 'value'),
        Input('wsave-input', 'value'),
        Input('networth-input', 'value'),
        Input('income-input', 'value'),
        Input('risk-input', 'value')
    ]
)
def update_risk_tolerance(n_clicks, age, education, married, kids, occupation, wsave, nw, income, risk):

    risk_tolerance = 0
    if n_clicks != None:
        X_inputs = [
            np.array([age, education, married, kids, occupation, wsave, nw, income, risk])]
        risk_tolerance = predict_risk_tolerance(model, X_inputs)

    return [round(float(risk_tolerance*100), 2)]


@app.callback(
    [
        # Ouputs
        Output('chart-allocation', 'figure'),
        Output('chart-performance', 'figure')
    ],
    [
        # Inputs
        Input('button-allocation', 'n_clicks'),
        Input('risk-tolerance-input', 'value'),

    ],
    [
        # State allows you to pass along extra values without firing the callbacks.
        State('ticker-symbols', 'value')
    ]
)
def display_asset_allocation(n_clicks, risk_tolerance, stock_tickers):

    allocated, returns = get_asset_allocation(risk_tolerance, stock_tickers)

    allocation_chart = {
        'data': [
            {
                'x': allocated.index,
                'y': allocated.iloc[:, 0] * 100,
                'type':'bar',
                'hovertemplate': '%{y:.2f}%<extra></extra>',
            }
        ],
        'layout': {
            'title': {
                'text': 'Suggested Asset Allocation',
                'x': 'Ticker symbols',
                'y': 'Percentage',
            },
            'xaxis': {'fixedrange': True},
            'yaxis': {
                'fixedrange': True,
                'ticksuffix': '%'
            },
            'colorway': ['#17B897'],  # chart color
            'height': 450,
            'width': 600
        }
    }

    performance_chart = {
        'data': [
            {
                'x': returns.index,
                'y': returns.iloc[:, 0],
                'type':'lines',
                'hovertemplate': '%{y:.2f}<extra></extra>',
            }
        ],
        'layout': {
            'title': {
                'text': 'Portfolio trend (Base: 100)',
                'x': 'Date',
                'y': 'Portfolio value',
            },
            'xaxis': {'fixedrange': True},
            'yaxis': {'fixedrange': True},
            'colorway': ['#E75480'],
            'height': 450,
            'width': 600
        }
    }

    return allocation_chart, performance_chart


# Run the constructed dashboard on a server (browser)
if __name__ == '__main__':
    app.run_server(debug=True)
