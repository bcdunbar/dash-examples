import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import MySQLdb # python 3
import pandas as pd

host = "enter host"
user="enter user"
passwd="enter password"
db="enter db"

app = dash.Dash()
server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3('Streaming MySQL example')
        ], className = "eight columns"),

        html.Div([
            html.Img(
                src=('https://s3-us-west-1.amazonaws.com/plotly-tutorials/'
                'logo/new-branding/dash-logo-by-plotly-stripe.png'),
                style={
                    'height': '100px',
                    'float': 'right'}),
        ], className = "four columns")
    ], className = "row"),

    html.Div([
        html.Div([
            dcc.Graph(id = 'graph-2', style={'height': '200px'}),
        ], className="twelve columns")
    ], className="row"),

    html.Div([
        html.Div(id='intermediate-value', style={'display': 'none'}),
        html.Div([
            dcc.Graph(id = 'graph'),
            dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
            )
        ], className="five columns"),

        html.Div([
            html.Table(id="table", style={'width':'100%'})
        ], className="five columns")
    ], className="row")

])


@app.callback(Output('intermediate-value', 'children'),
            [Input('interval-component', 'n_intervals')])
def clean_data(value):
     conn = MySQLdb.connect(host=host, user=user, passwd=password, db=db)
     cursor = conn.cursor()

     cursor.execute('SELECT * FROM stream.stream_table'); # change query accordingly
     rows = cursor.fetchall()
     df = pd.DataFrame( [[ij for ij in i] for i in rows] )

     df.rename(columns={0: 'date', 1: 'value'}, inplace=True);
     return df.to_json()

@app.callback(Output('table', 'children'),
            [Input('intermediate-value', 'children')])
def update_table(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data)
    dff = dff.sort_values(by=['date'], ascending=False)
    def make_dash_table(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row, style={'width':'100%'}))
        return table
    table = make_dash_table(dff[0:9])
    return table

@app.callback(Output('graph', 'figure'),
            [Input('intermediate-value', 'children')])
def update_graph(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data)
    figure = {
        'data': [{
            'type': 'histogram',
            'x': dff['value']
        }],
        'layout': {
            'margin': {
                'l':20,
                'r':20,
                'b':20,
                't':10
            }
        }
    }
    return figure

@app.callback(Output('graph-2', 'figure'), [Input('intermediate-value', 'children')])
def update_graph(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data)
    dff = dff.sort_values(by=['date'], ascending=True)
    figure = {
        'data': [{
            'x': dff['date'], # change accordingly
            'y': dff['value'] # change accordingly
        }],
        'layout': {
            'yaxis': {
                'zeroline': False
            },
            'margin': {
                'l':20,
                'r':20,
                'b':50,
                't':20
            }
        }
    }
    return figure

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

if __name__ == '__main__':
    app.run_server(debug=True)
