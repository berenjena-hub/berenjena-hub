# app/modules/dashboard/dashboard.py

from dash import Dash, dcc, html
import plotly.express as px

def create_dashboard(server):
    dash_app = Dash(
        __name__,
        server=server,
        url_base_pathname='/dashboard/'  # Esto define la ruta base de la app Dash
    )
    
    # Configuración del layout del dashboard
    dash_app.layout = html.Div([
        html.H1("Dashboard"),
        dcc.Graph(
            id='example-graph',
            figure=px.line(x=[1, 2, 3], y=[1, 4, 9], title="Example Chart")
        )
    ])

    return dash_app
