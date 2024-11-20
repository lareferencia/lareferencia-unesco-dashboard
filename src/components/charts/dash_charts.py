from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
#import translate
from translate.translate import translate
from data import get_unesco_objectives_and_count,get_subcategories_list_from_data_frame

#color palette for the pie charts
base_colors = [
    "#003f5c", "#2f4b7c", "#665191", "#a05195", 
    "#d45087", "#f95d6a", "#ff7c43", "#ffa600",
    "#33658a", "#86bbd8", "#4caf50", "#ffd166",
    "#ffe066", "#f28482", "#247ba0", "#c2c5aa",
    "#b56576", "#8ac926"
]



# Function to extend the color list
def extend_colors(base_colors, length):
    return base_colors * (length // len(base_colors)) + base_colors[:length % len(base_colors)]

#Subcategories distribution chart
def getSubcategoriesDistributionBarChart(df, lang):
    # Get subcategories dictionary
    subcategories_dict = get_subcategories_list_from_data_frame(df, lang)
    # Convert dictionary to DataFrame
    subcategories_df = pd.DataFrame(list(subcategories_dict.items()), columns=['subcategory', 'count'])
    # Save the full subcategory texts for hovertext, truncated to a maximum length
    hovertexts = subcategories_df['subcategory'].apply(lambda x: (x[:75] + '...') if len(x) > 75 else x)
    # X axis text, truncated to a maximum length
    x_subcategories = subcategories_df['subcategory'].apply(lambda x: (x[:15] + '...') if len(x) > 15 else x)
    # Extend the color list to match the number of subcategories
    colors = extend_colors(base_colors, len(subcategories_df))
    # Create the figure
    fig = go.Figure(
        data=[
            go.Bar(x=x_subcategories,
                   y=subcategories_df['count'],
                   hovertext=hovertexts,
                hovertemplate='%{y}<br>%{hovertext}<extra></extra>',
                   marker=dict(color=colors))
        ],
        layout=dict(
            title=translate(lang, 'Subcategories distribution'),
        )
    )
    
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    
    return dcc.Graph(figure=fig, config={
        'displaylogo': False,
        'modeBarButtonsToRemove': [
            'zoom2d',
            'pan2d',
            'select2d',
            'lasso2d',
            'zoomIn2d',
            'zoomOut2d',
            'autoScale2d',
            'resetScale2d',
        ]
    })

#Unesco objectives distribution chart
def getUnescoObjectivesDistributionBarChart(df,lang):
    #get Unesco objectives df
    objectives_df = get_unesco_objectives_and_count(df,lang)
    # Save the full subcategory texts for hovertext, truncated to a maximum length
    hovertexts = objectives_df['subcategory'].apply(lambda x: (x[:75] + '...') if len(x) > 75 else x)
    # Modify 'subcategory' to only contain the first three characters
    objectives_df['subcategory'] = objectives_df['subcategory'].str[:3]
    # Extend the color list to match the number of subcategories
    colors = extend_colors(base_colors, len(objectives_df))
    # Create the figure
    fig = go.Figure(
        data=[
            go.Bar(x=objectives_df['subcategory'],
                   y=objectives_df['count'],
                   hovertext=hovertexts,
                   hovertemplate='%{y}<br>%{hovertext}<extra></extra>',
                   marker=dict(color=colors))
        ],
        layout=dict(
            title=translate(lang, 'UNESCO objectives distribution'),
        )
    )
    return dcc.Graph(figure=fig,config={
        'displaylogo': False,
        'modeBarButtonsToRemove':[
            'zoom2d',
            'pan2d',
            'select2d',
            'lasso2d',
            'zoomIn2d',
            'zoomOut2d',
            'autoScale2d',
            'resetScale2d',
        ]})

'''
Options for this graph:
config={
    'displayModeBar': True,
    'modeBarButtonsToAdd': [
        'drawline',
        'drawopenpath',
        'drawclosedpath',
        'drawcircle',
        'drawrect',
        'eraseshape'
    ]
}
'''