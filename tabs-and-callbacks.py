import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from loremipsum import get_sentences
import numpy as np

app = dash.Dash()

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True

vertical = True

x = np.arange(1,11)
y = np.random.randint(10, size=(10))

theme = {
    'font': 'white',
    'background': 'rgb(80, 103, 132)',
    'lines': 'white',
    'trace': ['rgb(17, 157, 255)', 'rgb(13, 118, 191)', 'pink']
}

plot_layout = {
    'plot_bgcolor': theme['background'],
    'paper_bgcolor': theme['background'],
    'font': {'color': theme['font']},
    'margin': {
        'l': 30,
        'r': 30,
        'b': 30,
        't': 30
    },
    'xaxis': {
        'color': theme['lines']
    },
    'yaxis': {
        'range': [0,10],
        'color': theme['lines']
    },
    'legend': {'x': 0, 'y': 1}
}

app.layout = html.Div([
    # header
    html.Div([
        html.H3('Example of Dash Tabs')
    ]),
    # body
    html.Div(
        dcc.Tabs(
            tabs=[
                {'label': 'Updating Text', 'value': 1},
                {'label': 'Updating Data Attrs', 'value': 2},
                {'label': 'No Callbacks | Layout', 'value': 3},
                {'label': 'Something', 'value': 4},
            ],
            value=3,
            id='tabs',
            vertical=vertical,
            style={
                'height': '100vh',
                'color': 'white'
            }
        ),
        style={'width': '20%', 'float': 'left'}
    ),

    html.Div([
        # tab 1
        html.Div(
        [
            dcc.Input(id='my-id', value='initial value', type='text'),
            html.Div(id='my-div'),
            html.Div(id='tab-output')
        ], style={'display': 'none'}),

        # tab 2
        html.Div(
        [
            html.Div(id='tab-output')
        ], style={'display': 'none'}),

        # tab 3 - no callbacks
        html.Div(id="tab-output")

    ], style={'width': '80%', 'float': 'right'})

], style={
    'fontFamily': 'Sans-Serif',
    'margin-left': 'auto',
    'margin-right': 'auto',
})


@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):
    data = [{
        'x': x,
        'y': y,
        'marker': {
            'color': theme['trace'][2]
        },
        'type': 'scatter'
    }]

    if value == 1:
        tab_layout = html.Div([
            dcc.Input(id='my-id', value='initial value', type='text'),
            html.Div(id='my-div'),
            dcc.Graph(
                id='graph1',
                figure={
                    'data': data,
                    'layout': plot_layout
                }
            ),
            html.Div(' '.join(get_sentences(10)))
        ])
    elif value == 2:
        tab_layout = html.Div([
            dcc.Dropdown(
                id="dropdown-1",
                options=[{'label': 'Dodger', 'value': theme['trace'][0]},
                        {'label': 'Dodger Shade', 'value': theme['trace'][1]},
                        {'label': 'Pink', 'value': theme['trace'][2]}],
                value=theme['trace'][2]),
            dcc.Graph(
                id='graph2',
                figure={
                    'data': data,
                    'layout': plot_layout
                }
            )
        ])
    elif value == 3:
        tab_layout = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='wdcdecd',
                        figure={
                            'data': data,
                            'layout': plot_layout
                        },
                        style={'height': '300px'}
                    )
                ], className = "six columns"),
                html.Div([
                    dcc.Graph(
                        id='dfvmf',
                        figure={
                            'data': data,
                            'layout': plot_layout
                        },
                        style={'height': '300px'}
                    )
                ], className = "six columns")
            ], className = "row"),

            html.Div([
                html.Div([
                    dcc.Graph(
                        id='dmfvmf',
                        figure={
                            'data': data,
                            'layout': plot_layout
                        },
                        style={'height': '300px'}
                    )
                ], className = "six columns"),
                html.Div([
                    dcc.Graph(
                        id='khjbdf',
                        figure={
                            'data': data,
                            'layout': plot_layout
                        },
                        style={'height': '300px'}
                    )
                ], className = "six columns")
            ], className = "row")
        ])
    elif value == 4:
        tab_layout = html.Div([
            dcc.Graph(
                id='graph',
                figure={
                    'data': data,
                    'layout': plot_layout
                }
            ),
            html.Div(' '.join(get_sentences(10)))
        ])

    return tab_layout

@app.callback(
    Output('my-div', 'children'),
    [Input('my-id','value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

@app.callback(Output('graph2', 'figure'),
              [Input('dropdown-1', 'value')])
def update_output_1(value):
    data = [{
        'x': x,
        'y': y,
        'marker': {
            'color': value
        },
        'type': 'scatter'
    }]
    return {
        'data': data,
        'layout': plot_layout
    }

app.css.append_css({"external_url": "https://codepen.io/bcd/pen/mxaRvO.css"})

if __name__ == '__main__':
    app.run_server(debug=True)
