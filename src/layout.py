from dash import html,dcc
# import the translate function
from translate.translate import translate
# Bring dash chart
from components.charts.chart_container import get_chart_container
#bring language links component
from components.language_links import get_language_links
#Bring dropdowns
from components.dropdowns import get_dropdowns
#Bring ag_grid
from components.ag_grid import get_ag_grid
#Bring the modal
from components.modal import get_modal

#Select columns to exclude from the table
excluded_columns = ['PAIS', 'Nombre de la iniciativa','Detalles', 'WEB', 'CONTACTO']

#set language
lang = 'es'

#get language
def get_language():
    return lang
#set language
def set_language(l):
    global lang
    lang = l

def getLayout(categories_dropdown,data_frame,unesco_options):
    layout = html.Div(
        id='layout',
        children=[
        html.Meta(charSet='utf-8'),
        get_language_links(lang),
        get_dropdowns(data_frame, categories_dropdown, unesco_options,lang),
        get_chart_container(data_frame,lang),
            html.Div(
            style={'display':'flex'},
            children=[
                get_ag_grid(data_frame,excluded_columns,get_language),
                get_modal()
            ],
        className='header1'
        ),
    ], style={'padding': '20px'})
    return layout

