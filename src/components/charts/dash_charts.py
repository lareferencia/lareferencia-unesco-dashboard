from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
#import translate
from translate.translate import translate
from data import get_unesco_objectives_and_count

#Country distribution chart
def getCountryDistributionPieChart(df,lang):
    fig = px.pie(df, names='PAIS', title=translate(lang, 'Country distribution'))
    graph = dcc.Graph(figure=fig)
    return graph

#Subcategories distribution chart
def getSubcategoriesDistributionPieChart(df,lang):
    fig = px.pie(df, names='Subcategory', title=translate(lang, 'Subcategories distribution'))
    graph = dcc.Graph(figure=fig)
    return graph

#Unesco objectives distribution chart
def getUnescoObjectivesDistributionBarChart(df,lang):
    #get Unesco objectives df
    objectives_df = get_unesco_objectives_and_count(df,lang)
    # Save the full subcategory texts for hovertext, truncated to a maximum length
    hovertexts = objectives_df['subcategory'].apply(lambda x: (x[:75] + '...') if len(x) > 75 else x)
    # Modify 'subcategory' to only contain the first three characters
    objectives_df['subcategory'] = objectives_df['subcategory'].str[:3]
    # Create a list of colors, same as the pie charts 
    colors = px.colors.qualitative.Plotly * (len(objectives_df) // len(px.colors.qualitative.Plotly)) + \
              px.colors.qualitative.Plotly[:len(objectives_df) % len(px.colors.qualitative.Plotly)]
    # Create the figure
    fig = go.Figure(
        data=[
            go.Bar(x=objectives_df['subcategory'],
                   y=objectives_df['count'],
                   hovertext=hovertexts,
                   marker=dict(color=colors))
        ],
        layout=dict(
            title=translate(lang, 'UNESCO objectives distribution'),
        )
    )
    return dcc.Graph(figure=fig, config={
    'displayModeBar': True,
    'modeBarButtonsToAdd': [
        'drawline',
        'drawopenpath',
        'drawclosedpath',
        'drawcircle',
        'drawrect',
        'eraseshape'
    ]
})