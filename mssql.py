import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import pyodbc
import pandas as pd

## Connect to Microsoft SQL Server
conn = pyodbc.connect("Driver={SQL Server};"
                      "Server=test-mssql.cwwxgcilxwxw.us-west-2.rds.amazonaws.com;"
                      "UID=masteruser;PWD=connecttoplotly;"
                      "Database=plotly_datasets;")
cursor = conn.cursor()

# Fetch data
cursor.execute('SELECT * FROM apple_stock_2014');
rows = cursor.fetchall()

df = pd.DataFrame( [[ij for ij in i] for i in rows] )
df.rename(columns={0: 'x', 1: 'y'}, inplace=True);

app = dash.Dash()
server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3('Basic Microsoft SQL Server Example')
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
        dcc.Graph(
            id = 'graph',
            figure = {
                'data': [{
                    'x': df['x'],
                    'y': df['y']
                }],
                'layout': {
                    'title':'Apple Stock 2014 from Microsoft SQL Server',
                    'xaxis': dict( title='Date' ),
                    'yaxis': dict( title='$' )
                }
            }
        )
    ])
])

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

if __name__ == '__main__':
    app.run_server(debug=True)
