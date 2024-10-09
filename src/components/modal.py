import dash_bootstrap_components as dbc

def get_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader(id='modal-header'),
            dbc.ModalBody(id='modal-body'),
            dbc.ModalFooter(dbc.Button("Close", id="row-selection-modal-close", className="ml-auto"),style={'display':'none'}),
        ],
        id='modal',
        size='lg',
        centered=True,
        is_open=False,
    )