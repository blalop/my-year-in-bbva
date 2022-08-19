import plotly.express as px
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output

from operations import Operations


operations = Operations()

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="BBVA Account"),
        dcc.Graph(
            id="balance",
            figure=px.line(operations.all, x="date", y="balance"),
        ),
        html.H2(children="Transactions by year (€)"),
        dcc.Graph(id="by-year", figure=px.bar(operations.by_year)),
        html.H2(children="Transactions by month (€)"),
        html.P(children="Click in incoming/spending to see the details by month"),
        dcc.Graph(id="grouped-by-month", figure=px.bar(operations.by_month)),
        html.Div(id="query-by-month"),
        html.H2(children="Transactions by concept (€)"),
        html.P(children="Click in incoming/spending to see the details by concept"),
        dcc.Graph(id="grouped-by-concept", figure=px.bar(operations.by_concept)),
        html.Div(id="query-by-concept"),
    ]
)


@app.callback(
    Output("query-by-month", "children"), Input("grouped-by-month", "clickData")
)
def update_month(click_data):
    if not click_data:
        return

    month = click_data["points"][0]["label"]
    amount = click_data["points"][0]["value"]

    operations_by_month = operations.query_by_month(month, amount)
    return dash_table.DataTable(operations_by_month.to_dict("records"))


@app.callback(
    Output("query-by-concept", "children"), Input("grouped-by-concept", "clickData")
)
def update_concept(click_data):
    if not click_data:
        return

    concept = click_data["points"][0]["label"]
    amount = click_data["points"][0]["value"]

    operations_by_concept = operations.query_by_concept(concept, amount)
    return dash_table.DataTable(operations_by_concept.to_dict("records"))
