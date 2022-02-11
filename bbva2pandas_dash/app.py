import plotly.express as px
from dash import Dash, html, dcc

from bbva2pandas_dash.operations import Operations


class Bbva2PandasDash:
    def __init__(self, path):
        self.app = Dash(__name__)
        self.operations = Operations(path)

        self.app.layout = html.Div(
            children=[
                html.H1(children="BBVA Account"),
                dcc.Graph(
                    id="balance",
                    figure=px.line(self.operations.operations, x="date", y="balance"),
                ),
                dcc.Graph(id="by_year", figure=px.bar(self.operations.by_year)),
                dcc.Graph(id="by_month", figure=px.bar(self.operations.by_month)),
                dcc.Graph(id="by_concept", figure=px.bar(self.operations.by_concept)),
            ]
        )

    def start(self):
        self.app.run_server(debug=True)
