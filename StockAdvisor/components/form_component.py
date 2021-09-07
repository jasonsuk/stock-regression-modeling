from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


# Feature 1: AGE
age_input = dbc.FormGroup(
    [
        dbc.Label('1. Select your age group', html_for='slider',
                  className='survey-question'),
        dcc.Slider(
            id='age-input',
            min=10,
            max=100,
            step=10,
            value=30,
            marks={i: str(i) for i in range(10, 100+10, 10)}
        ),
        dbc.FormText("For example, if you are 20 - 29, select 20",
                     className='survey-desc'),
    ]
)


# Feature 2: EDUCATION
education_input = dbc.FormGroup(
    [
        dbc.Label('2. Select your education group',
                  html_for='dropdown', className='survey-question'),
        dcc.Dropdown(
            id='education-input',
            options=[
                {'label': '1: No High School Degree', 'value': 1},
                {'label': '2: High School Degree', 'value': 2},
                {'label': '3: Associate Degree', 'value': 3},
                {'label': '4: College Degree', 'value': 4}
            ],
            value=1
        ),
        dbc.FormText(
            "For example, if post graduate falls into 4: College Degree", className='survey-desc'),
    ]
)

# Feature 3: MARRIED
married_input = dbc.FormGroup(
    [
        dbc.Label('3. Select your marital status',
                  className='survey-question'),
        dbc.RadioItems(
            id='married-input',
            options=[
                {'label': 'Married', 'value': 1},
                {'label': 'Not Married', 'value': 2},
            ],
            value=1
        ),
        dbc.FormText("'Not Married' includes all marital status besides being married."
                     "For example, it includes seperated, divorced, etc.", className='survey-desc'),
    ]
)

# Feature 4: KIDS
kids_input = dbc.FormGroup(
    [
        dbc.Label('4. Select mumber of your kids',
                  className='survey-question'),
        dbc.Input(
            id='kids-input',
            type='number',
            min=0,
            step=1,
            value=0
        ),
    ]
)

# Feature 5: OCCUPATION
occupation_input = dbc.FormGroup(
    [
        dbc.Label('5. Select the level of your occupation',
                  html_for='dropdown', className='survey-question'),
        dcc.Dropdown(
            id='occupation-input',
            options=[
                {'label': '1: Managerial', 'value': 1},
                {'label': '2: Supervisory', 'value': 2},
                {'label': '3: Entry-level / Associate', 'value': 3},
                {'label': '4: Unemployed', 'value': 4}
            ],
            value=1
        ),
        dbc.FormText("Part-time employees are considered as employeed",
                     className='survey-desc'),
    ]
)

# Feature 6: WSAVE - SPENDING HABIT
wsave_input = dbc.FormGroup(
    [
        dbc.Label(className='survey-question',
                  children='6. Select one that is closest to your spending habit', html_for='dropdown'),
        dbc.FormText("Hint: Reflect on your habit last 6 months",
                     className='survey-desc'),
        dcc.Dropdown(
            id='wsave-input',
            options=[
                {'label': '1: I spent more than my income', 'value': 1},
                {'label': '2: I spent similar to my income', 'value': 2},
                {'label': '3: I spent less than my income', 'value': 3},
            ],
            value=1
        )
    ]
)

# Feature 7: NETWORTH
networth_input = dbc.FormGroup(
    [
        dbc.Label('7. Select your net worth', html_for='slider',
                  className='survey-question'),
        dcc.Slider(
            id='networth-input',
            className='slider network-slider',

            # Arbitrary numbers used here
            min=-2000000,
            max=3000000,
            marks={
                -2000000: '-$2M',
                -1000000: '-$1M',
                0: '$0',
                500000: '$500k',
                1000000: '$1M',
                2000000: '$2M+',
            },
            value=10000,
            updatemode='drag',
            tooltip={'always_visible': True}
        ),
    ]
)

# Feature 8: INCOME
income_input = dbc.FormGroup(
    [
        dbc.Label('8. Select your income', html_for='slider',
                  className='survey-question'),
        dcc.Slider(
            id='income-input',
            className='slider income-slider',

            # Arbitrary numbers used here
            min=-1000000,
            max=2000000,
            marks={
                -1000000: '-$1M',
                0: '$0',
                1000000: '$1M',
                2000000: '$2M+',
            },
            value=10000,
            updatemode='drag',
            tooltip={'always_visible': True}

        ),
    ]
)

# Feature 9: WILLINGNESS TO TAKE RISK
risk_input = dbc.FormGroup(
    [
        dbc.Label('9. How much are you willing to take risk in general?', className='survey-question',
                  html_for='dropdown'),
        dcc.Dropdown(
            id='risk-input',
            options=[
                {'label': '1: Very likely', 'value': 1},
                {'label': '2: Somewhat likely', 'value': 2},
                {'label': '3: Unlikely', 'value': 3},
                {'label': '4: Never', 'value': 4}
            ],
            value=1
        ),
    ]
)


# Button to submit the inputs
button_input_submit = dbc.Button(id='button-risktolerance',
                                 className='button button-risktolerance',
                                 children='Calculate my risk tolerance',
                                 color="primary",
                                 block=True)

# Create a form component

form = dbc.Form(
    className='form-container',
    children=[
        age_input, education_input, married_input, kids_input, occupation_input,
        wsave_input, networth_input, income_input, risk_input, button_input_submit
    ]
)
