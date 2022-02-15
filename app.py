#!/usr/bin/env python3

import argparse
import plotly.express as px
from dash import Dash, html, dcc, dash_table
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
        dcc.Graph(id="by-year", figure=px.bar(operations.group_by_year)),
        dcc.Graph(id="grouped-by-month", figure=px.bar(operations.group_by_month)),
        html.Div(id="query-by-month"),
        dcc.Graph(id="grouped-by-concept", figure=px.bar(operations.group_by_concept)),
        html.Div(id="query-by-concept"),
    ]
)


@app.callback(
    Output("query-by-concept", "children"), Input("grouped-by-concept", "clickData")
)
def update_concept(click_data):
    if not click_data:
        return

    concept = click_data["points"][0]["label"]
    amount = click_data["points"][0]["value"]
    type = "incoming" if amount > 0 else "spending"

    operations_by_concept = operations.query_by_concept(concept, type)
    return dash_table.DataTable(operations_by_concept.to_dict("records"))


@app.callback(
    Output("query-by-month", "children"), Input("grouped-by-month", "clickData")
)
def update_month(click_data):
    if not click_data:
        return

    month = click_data["points"][0]["label"][:7]
    amount = click_data["points"][0]["value"]
    type = "incoming" if amount > 0 else "spending"

    operations_by_month = operations.query_by_month(month, type)
    return dash_table.DataTable(operations_by_month.to_dict("records"))


if __name__ == "__main__":
    app.run_server(debug=debug)
