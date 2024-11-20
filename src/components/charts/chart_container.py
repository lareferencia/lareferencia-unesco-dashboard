from dash import html
from components.charts.dash_charts import getSubcategoriesDistributionBarChart, getUnescoObjectivesDistributionBarChart

def get_chart_div(chart_id, chart_content):
    return html.Div(
        id=chart_id,
        style={'width': '100%'},
        children=[chart_content]
    )

def get_chart_container(data_frame,lang):
    return html.Div(
        id='chart-container',
        style={'background-color': '#CFD8DC', 'display': 'flex', 'height': 'fit-content', 'flex-direction': 'row'},
        children=[
            get_chart_div('subcategoriesChart', getSubcategoriesDistributionBarChart(data_frame,lang)),
            get_chart_div('unescoChart', getUnescoObjectivesDistributionBarChart(data_frame,lang)),
        ]
    )