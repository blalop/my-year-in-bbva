import configparser
import glob

import plotly.express as px
import pandas as pd
import bbva2pandas as b2p

from dash import Dash, html, dcc

def load_data(path):
    documents = glob.glob(f'{path}/*.pdf')
    dataframes = map(lambda x: b2p.Report(x).to_df(), documents)
    return pd.concat(dataframes)

def load_config(filename='config.ini'):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

config = load_config()
operations = load_data(config['bbva2pandas']['DocumentPath'])

incoming = operations.query('amount > 0')
spending = operations.query('amount < 0')

def group_amount_by_year(dataframe):
    dataframe_by_year = dataframe.groupby(dataframe.date.dt.year).sum()
    dataframe_by_year.index = dataframe_by_year.index.to_flat_index()
    return dataframe_by_year.drop('balance', 1).squeeze()

by_year = {
    'incoming': group_amount_by_year(incoming),
    'spending': group_amount_by_year(spending),
    'difference': group_amount_by_year(incoming) + group_amount_by_year(spending)
}

def group_amount_by_month(dataframe):
    dataframe_by_month = dataframe.groupby([(dataframe.date.dt.year),(dataframe.date.dt.month)]).sum()
    dataframe_by_month.index = dataframe_by_month.index.to_flat_index().map(lambda x: f'{str(x[0])[2:]}-{x[1]}')
    return dataframe_by_month.drop('balance', 1).squeeze()

by_month = {
    'incoming': group_amount_by_month(incoming),
    'spending': group_amount_by_month(spending),
    'difference': group_amount_by_month(incoming) + group_amount_by_month(spending)
}

def group_amount_by_concept(dataframe):
    dataframe_by_concept = dataframe.groupby(dataframe.concept).sum()
    return dataframe_by_concept.drop('balance', 1).squeeze()

by_concept = {
    'incoming': group_amount_by_concept(incoming),
    'spending': group_amount_by_concept(spending),
    'difference': group_amount_by_concept(incoming) + group_amount_by_concept(spending)
}

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='BBVA Account'),

    dcc.Graph(
        id='balance',
        figure=px.line(operations, x="date", y="balance")
    ),

    dcc.Graph(
        id='by_year',
        figure=px.bar(pd.concat(by_year, axis=1))
    ),

    dcc.Graph(
        id='by_month',
        figure=px.bar(pd.concat(by_month, axis=1))
    ),

    dcc.Graph(
        id='by_concept',
        figure=px.bar(pd.concat(by_concept, axis=1))
    )

])
