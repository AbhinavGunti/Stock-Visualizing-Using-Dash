from dash import dash, html, dcc, ctx
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
                dcc.Input(id="stock-code",type='text'),
                html.Button('Submit',id="submit-stock-code",n_clicks=0)
            ]),
            html.Div([
                html.Br(),
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    min_date_allowed=dt(2021,1,1),
                    max_date_allowed=dt(2022, 6, 1),
                    start_date_placeholder_text='MM/DD/YYYY',
                    end_date_placeholder_text='MM/DD/YYYY',
                    # initial_visible_month=dt(2022, 1, 1)
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
                    html.Div([html.Img(id='logo-img',src="https://i.pinimg.com/originals/f5/05/24/f50524ee5f161f437400aaf215c9e12f.jpg"),                
                    html.P(id='short-name')],id="company-header"),
                  ],
                className="header",id="logo_company_name"),
            html.Div( #Description
                    [
                        html.P(id='long-buisness-summary')
                    ],
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
    Output("description","children"),),
    State("stock-code","value"),
    Input("submit-stock-code","n_clicks")
)
def company_info(val,btn1):
    changed_id2 = [p['prop_id'] for p in ctx.triggered][0]
    if 'submit-stock-code' in changed_id2:
        ticker = yf.Ticker(val)
        inf = ticker.info
        df = pd.DataFrame().from_dict(inf, orient="index").T
        return df.logo_url[0],df.shortName[0],df.longBusinessSummary[0]
        # df's first element of 'longBusinessSummary', df's first element value of 'logo_url', df's first element value of 'shortName'
    else:
        return "https://i.pinimg.com/originals/f5/05/24/f50524ee5f161f437400aaf215c9e12f.jpg","",""
@app.callback(
    Output("graphs-content","children"),
    State("stock-code","value"),
    State("my-date-picker-range","start_date"),
    State("my-date-picker-range","end_date"),
    Input("submit-stock-price","n_clicks")
)
def graph(input,sd,ed,btn2):
    changed_id2 = [p['prop_id'] for p in ctx.triggered][0]
    if 'submit-stock-price' in changed_id2:
        df = yf.download(input,sd,ed)
        df.reset_index(inplace=True)
        fig = get_stock_price_fig(df)
        return dcc.Graph(figure=fig)
    else:
        return ""
    # plot the graph of fig using DCC function

def get_stock_price_fig(df):
    fig = px.line(df,x= "Date",y= ["Open","Close"],title="Closing and Opening Price vs Date")
    return fig
@app.callback(
    Output("main-content","children"),
    State("stock-code","value"),
    State("my-date-picker-range","start_date"),
    State("my-date-picker-range","end_date"),
    Input("submit-indicators","n_clicks")
)
def graph(input,sd,ed,btn2):
    changed_id2 = [p['prop_id'] for p in ctx.triggered][0]
    if 'submit-indicators' in changed_id2:
        df = yf.download(input,sd,ed)
        df.reset_index(inplace=True)
        fig = get_more(df)
        return dcc.Graph(figure=fig)
    else:
        return ""
    # plot the graph of fig using Exponential Moving Average(EMA) function
def get_more(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,x="Date",y="EWA_20",title="Exponential Moving Average vs Date")
    fig.update_traces(mode="lines+markers+text")#lines,markers,text
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)