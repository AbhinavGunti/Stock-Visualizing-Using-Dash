from dash import dash, html, dcc, callback_context
from datetime import datetime as dt
from dash.dependencies import Input, Output, State


import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([html.Div(
          [
            html.P("Welcome to the Stock Dash App!", id="start"),
            html.Div([
                html.Label("Input Stock Code : ",id="stock_code_label"),
                html.Br(),
                dcc.Input(id="stock-code",type='text',value="AAPL"),
                html.Button('Submit',id="submit-stock-code",n_clicks=0)
            ]),
            html.Div([
                html.Br(),
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    min_date_allowed=dt(2022,1,1),
                    max_date_allowed=dt(2022, 6, 1),
                    initial_visible_month=dt(2022, 1, 1),
                    end_date=dt(2022, 6, 1)
                    )            
                ]),
            html.Div([
                html.Br(),
                html.Button('Stock Price',id="submit-stock-price",n_clicks=0),
                html.Button('Indicators',id="submit-indicators",n_clicks=0),
                html.Br(),
                dcc.Input(id="number-of-days",type='text',placeholder="Number of days"),
                html.Button('Forecast',id="submit-forecast",n_clicks=0)


            ]),
          ],
        className="inputs"),
        html.Div(
          [
            html.Div(
                  [  # Logo
                    # Company Name
                    html.Div([html.Img(id='logo-img',src=""),                
                    html.P(id='short-name')],id="company-header"),
                    html.P(id='long-buisness-summary')
                  ],
                className="header",id="logo_company_name"),
            html.Div( #Description
              id="description", className="decription_ticker"),
            html.Div([
                # Stock price plot
            ], id="graphs-content"),
            html.Div([
                # Indicator plot
            ], id="main-content"),
            html.Div([
                # Forecast plot
            ], id="forecast-content")
          ],
        className="content")],
        className="container")
@app.callback(
    (Output("logo-img","src"),
    Output("short-name","children"),
    Output("long-buisness-summary","children"),),
    State("stock-code","value"),
    Input("submit-stock-code","n_clicks")
)
def company_info(val,btn1):
    ticker = yf.Ticker(val)
    inf = ticker.info
    df = pd.DataFrame().from_dict(inf, orient="index").T
    return df.logo_url[0],df.shortName[0],df.longBusinessSummary[0]
    # df's first element of 'longBusinessSummary', df's first element value of 'logo_url', df's first element value of 'shortName'
if __name__ == '__main__':
    app.run_server(debug=True)