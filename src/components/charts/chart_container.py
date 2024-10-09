from dash import html
from components.charts.dash_charts import getDashPieChart

def get_chart_div(chart_id, chart_content):
    return html.Div(
        id=chart_id,
        style={'width': '100%'},
        children=[chart_content]
    )

def get_chart_container():
    return html.Div(
        id='chart-container',
        style={'background-color': '#CFD8DC', 'display': 'flex', 'height': 'fit-content', 'flex-direction': 'row'},
        children=[
            get_chart_div('chart1', getDashPieChart()),
            get_chart_div('chart2', html.Span('Chart 2')),
            get_chart_div('chart3', html.Span('Chart 3')),
        ]
    )