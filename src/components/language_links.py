from dash import html, dcc

def get_language_links(lang):
    return html.Div(
        style={
            'display':'flex',
            'justify-content':'end','gap':'10px'
            ,'padding':'10px',},
        children=[
            html.A(
                    'EN',
                    id='english-link',
                    href='#',
                    style={'cursor': 'pointer', 'width': '30px'},
                    title='English',
                    n_clicks=0
                ),
            html.A(
                    'ES',
                    id='spanish-link',
                    href='#',
                    style={'cursor': 'pointer', 'width': '30px'},
                    title='Español',
                    n_clicks=0
            ),
            dcc.Store(id='language-store', data=lang)
    ])