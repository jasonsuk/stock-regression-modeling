from dash import dcc
from dash import html

risk_tolerance_output = html.Div(
    className='risk-tolerance-output',
    children=[
        html.H3('Your calculated risk tolerance is (scale of 100)...'),
        # output will be used as an input for allocation component
        dcc.Input(id='risk-tolerance-input',
                  disabled=True, className='risk-tolerance-input')
    ])
