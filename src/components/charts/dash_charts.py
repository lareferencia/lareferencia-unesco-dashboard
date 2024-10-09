from dash import dcc
import plotly.graph_objects as go

def getDashChart():
    graph = dcc.Graph(
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
    return graph


# Example or pie chart
def getDashPieChart():
    fig = go.Figure(data=[go.Pie(labels=['Label1', 'Label2', 'Label3'], values=[1, 2, 3])])
    graph = dcc.Graph(figure=fig)
    return graph