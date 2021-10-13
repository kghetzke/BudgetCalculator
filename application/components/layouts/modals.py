import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

from application.components.datasteps.datasteps import budget_item


def budget_item_entry_modal():
    modal = dbc.Modal(
        id = "budget_item_modal",
        children = [
            html.Div([], id = "modal_content"),
            dbc.ModalFooter(
                [dbc.Button("Cancel", id = "modal_cancel_button"),
                dbc.Button("Save", id = "modal_save_button")]
            ),
            dcc.Store('modal_fields_dump', data = None)
        ]
    )
    return modal

def json_modal():
    modal = dbc.Modal(
        id = "json_modal",
        children = [
            dbc.ModalHeader("Edit Budget"),
            dcc.Textarea(id = 'json_edit_text', style = {'height': 500}),
            dbc.ModalFooter(
                [dbc.Button("Cancel", id = "json_cancel_button"),
                dbc.Button("Save", id = "json_save_button")]
            ),
        ],
        size = "xl"
    )
    return modal


month_days = [
    {'label': '1 - First', 'value': 1},
    {'label': '2 - Second', 'value': 2},
    {'label': '3 - Third', 'value': 3},
    {'label': '4 - Fourth', 'value': 4},
    {'label': '5 - Fifth', 'value': 5},
    {'label': '6 - Sixth', 'value': 6},
    {'label': '7 - Seventh', 'value': 7},
    {'label': '8 - Eighth', 'value': 8},
    {'label': '9 - Ninth', 'value': 9},
    {'label': '10 - Tenth', 'value': 10},
    {'label': '11 - Eleventh', 'value': 11},
    {'label': '12 - Twelvth', 'value': 12},
    {'label': '13 - Thirteenth', 'value': 13},
    {'label': '14 - Fourteenth', 'value': 14},
    {'label': '15 - Fifteenth', 'value': 15},
    {'label': '16 - Sixteenth', 'value': 16},
    {'label': '17 - Seventeenth', 'value': 17},
    {'label': '18 - Eighteenth', 'value': 18},
    {'label': '19 - Nineteenth', 'value': 19},
    {'label': '20 - Twentieth', 'value': 20},
    {'label': '21 - Twenty-First', 'value': 21},
    {'label': '22 - Twenty-Second', 'value': 22},
    {'label': '23 - Twenty-Third', 'value': 23},
    {'label': '24 - Twenty-Fourth', 'value': 24},
    {'label': '25 - Twenty-Fifth', 'value': 25},
    {'label': '26 - Twenty-Sixth', 'value': 26},
    {'label': '27 - Twenty-Seventh', 'value': 27},
    {'label': '28 - Twenty-Eighth', 'value': 28},
    {'label': 'Last-Day', 'value': 'last'}]

week_days = [
    {'label': 'Monday', 'value': 'Monday'},
    {'label': 'Tuesday', 'value': 'Tuesday'},
    {'label': 'Wednesday', 'value': 'Wednesday'},
    {'label': 'Thursday', 'value': 'Thursday'},
    {'label': 'Friday', 'value': 'Friday'},
    {'label': 'Saturday', 'value': 'Saturday'},
    {'label': 'Sunday', 'value': 'Sunday'},]

def day_selection_dropdowns(recurrence, set_val: budget_item=None):
    if recurrence == 'monthly':
        text = dbc.Label("Day of Recurrence")
        dropdown = dcc.Dropdown(id = {"type": "modal_field", "index": 'modal_date'},
            options=month_days,
            value = set_val.item['day'] if set_val is not None else None
        )
        return html.Div([text, dropdown])
    elif recurrence == 'weekly':
        text = dbc.Label("Day of Recurrence")
        dropdown = dcc.Dropdown(id = {"type": "modal_field", "index": 'modal_date'},
            options=week_days,
            value = set_val.item['day'] if set_val is not None else None
        )
        return html.Div([text, dropdown])
    elif recurrence == 'daily':
        return
    elif recurrence == 'one_off':
        text = dbc.Label("Input Date (MM-DD-YYYY)")
        dropdown = dbc.Input(id = {"type": "modal_field", "index": 'modal_date'}, type = 'text', value = set_val.item['date'] if set_val is not None else None)
        return html.Div([text, dropdown])


default_expense = budget_item('expense','monthly',{'day': 1, 'value': 0, 'description': 'Add description here', 'category': 'add category tag here'})

def fill_modal(item: budget_item=default_expense, edit_state: bool=False):
    header_text = "Budget Item: " + str(item.type).title()
    header = dbc.ModalHeader(header_text)
    caches = html.Div([dcc.Store(id = {"type": "modal_cache", "index": "original_item_cached"}, data = item.__dict__),
        dcc.Store(id = {"type": "modal_cache", "index": "edit_state"}, data=edit_state)])
    if item.type == 'expenses' or item.type=='income':
        modal_content = dbc.ModalBody(
                [dcc.Dropdown(id = {"type": "modal_field", "index": "modal_recurrence"}, 
                    options = [{'label': cat.title(), 'value': cat} for cat in ['monthly','weekly','daily','one_off']],
                    value = item.subtype
                    ),
                html.Div([day_selection_dropdowns(item.subtype, item)], id = "recurring_date_selector"),
                dbc.Label("Description"),
                dbc.Input(id = {"type": "modal_field", "index": "modal_description"}, type='text', value = item.item['description']),
                dbc.Label("Value"),
                dbc.Input(id = {"type": "modal_field", "index": "modal_value"}, type='number', value = item.item['value'])
                ]
            )
    elif item.type == 'milestones':
        modal_content = dbc.ModalBody(
            [dbc.Label("Input Date (MM-DD-YYYY)"),
            dbc.Input(id = {"type": "modal_field", "index": 'modal_date'}, type = 'text', value = item.item['date']),
            dbc.Label("Description"),
            dbc.Input(id = {"type": "modal_field", "index": "modal_description"}, type='text', value = item.item['description']),
            dbc.Label("Value"),
            dbc.Input(id = {"type": "modal_field", "index": "modal_value"}, type='number', value = item.item['value'])]
        )
    else:
        modal_content = html.Div(['nothing yet'])
    return [header,modal_content,caches]

