from dash import html, dcc
from translate.translate import translate

def get_countries_dropdown(data_frame, lang):
    return dcc.Dropdown(
        id='countries-dropdown',
        options=[{'label': pais, 'value': pais} for pais in data_frame['PAIS'].unique()],
        multi=True,
        placeholder=translate(lang, u'Select_a_country'),
        style={'width': '100%'}
    )

def get_column_dropdown(categories_dropdown, lang):
    return dcc.Dropdown(
        id='column-dropdown',
        options=categories_dropdown,
        placeholder=translate(lang, 'Select_a_category'),
        multi=True,
        style={'width': '100%'}
    )

def get_objetivos_dropdown(unesco_options, lang):
    return dcc.Dropdown(
        id='objetivos-dropdown',
        options=unesco_options,
        placeholder=translate(lang, 'Select_an_UNESCO_objective'),
        multi=True,
    )

def get_dropdowns(data_frame, categories_dropdown, unesco_options, lang):
    dropdowns = html.Div(
        [
            html.Div(
                [
                    html.Div([get_countries_dropdown(data_frame, lang)], style={'width': '30%'}),
                    html.Div([get_column_dropdown(categories_dropdown, lang)], style={'flex': '1'}),
                ], 
                style={ 'background-color': '#CFD8DC', 'display': 'flex'}
            ),
            html.Div([get_objetivos_dropdown(unesco_options, lang)], style={'width':'100%'})
        ],
        style={'display':'flex','flex-direction':'column'}
    )
    return dropdowns