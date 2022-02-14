#!/usr/bin/env python3

import argparse
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from operations import Operations


def parse_args():
    parser = argparse.ArgumentParser(description="Prints BBVA reports PDF files")
    parser.add_argument("directory", help="Directory of the PDF files")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    return args.directory, args.debug


directory, debug = parse_args()

operations = Operations(directory)

app = Dash(__name__)
app.layout = html.Div(
    children=[
        html.H1(children="BBVA Account"),
        dcc.Graph(
            id="balance",
            figure=px.line(operations.operations, x="date", y="balance"),
        ),
        dcc.Graph(id="by-year", figure=px.bar(operations.by_year)),
        dcc.Graph(id="by-month", figure=px.bar(operations.by_month)),
        dcc.Graph(id="by-concept", figure=px.bar(operations.by_concept)),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=debug)
