import dash_ag_grid as dag
from translate.translate import translate

def get_ag_grid(data_frame,excluded_columns,get_language):
    return dag.AgGrid(
        id='data-table',
        columnDefs=[
            {'headerName': translate(get_language(),col), 
                'field': col,
                'filter': True if col in ['PAIS','Nombre de la iniciativa'] else None,
                'sortable': True if col == 'PAIS' else False,
                'cellRenderer': "ContactoButton" if col == 'CONTACTO' else
                "WebButton" if col == 'WEB' else
                "IniciativaComponent" if col == 'Nombre de la iniciativa' else 
                "DetallesComponent" if col == 'Detalles' else None,
                'maxWidth': 120 if col =='Detalles' else 
                            100 if col == 'WEB' else None,
                'minWidth': 650 if col == 'Nombre de la iniciativa' else 
                            125 if col == 'PAIS' else 
                            120 if col == 'Detalles' else None,
                }
            for col in excluded_columns
        ],
        rowData=data_frame[excluded_columns].to_dict('records'),
        className="ag-theme-material",
        columnSize='responsiveSizeToFit',
        dashGridOptions={
            'pagination': True,
            'paginationAutoPageSize': True,
            "icons": {
                'menu': '<i class="fa fa-search" aria-hidden="true"></i>',
            }
        },
        defaultColDef={
            'resizable': True,
        },
        getRowStyle = {
        "styleConditions": [
            {
            "condition": "params.rowIndex % 2 === 0",
            "style": {"backgroundColor": "#CFD8DC"},
        },
    ]
    },
    style={'height': '800px'}
    )