from dash import dash, html, dcc, ctx
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
from numpy import ediff1d


import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from datetime import datetime, timedelta

app = dash.Dash(__name__)

@app.callback(
    Output("forecast-content","children"),
    State("stock-code","value"),
    State("number-of-days","value"),
    Input("Forecast","n_clicks")
)
def graph(input,day,btn3):
    changed_id2 = [p['prop_id'] for p in ctx.triggered][0]
    if 'submit-indicators' in changed_id2:
        end_date = datetime.today()
        end_date=end_date.strftime("%m/%d/%Y")
        start_date = datetime.today() - timedelta(days=day)
        start_date=start_date.strftime("%m/%d/%Y")
        df = yf.download(input,start_date,end_date)
        df.reset_index(inplace=True)
        fig = get_forecast(df)
        return dcc.Graph(figure=fig)
    # plot the graph of fig using Exponential Moving Average(EMA) function
def get_forecast(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,x="Date",y="EWA_20",title="Exponential Moving Average vs Date")
    fig.update_traces(mode="lines+markers+text")#lines,markers,text
    return fig