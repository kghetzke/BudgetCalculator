import io
import json
from datetime import datetime
import pandas as pd
import plotly.express as px

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, ALL, MATCH

from application.app import app
import  application.components.datasteps.graphs as app_graphs
from application.components.datasteps.datasteps import Budget, budget_item
from application.components.layouts.modals import day_selection_dropdowns, fill_modal

### Tab 1 Callbacks ###

# First, some callbacks to fill in the budget items
@app.callback(
    Output('income_items_container','children'),
    Output('expense_items_container','children'),
    Output('milestones_container','children'),
    Input('main_budget','data')
)
def fill_tables(budget):
    my_budget = Budget(budget)
    income_items = html.Div([
        html.Div([
            html.Div(" ",style = {'width': '5%'}),
            html.Div(var.title(), style = {'width': '15%'}),
            html.Div([
                html.Div([
                    html.Div(entry['description'], style = {'width':'65%', 'text-align': 'left'}),
                    html.Div("$" + str(entry['value']), style = {'width':'25%', 'text-align': 'left'}),
                    html.Button("E",id = {'type': 'edit_income', 'index': var +'__'+ str(idx)}),
                    html.Button("X",id = {'type': 'remove_income', 'index': var +'__'+ str(idx)}),
                ], style = {'display': 'flex'})
            for idx, entry in enumerate(my_budget.income[var])], style = {'width': '80%'})
        ], style = {'display': 'flex'})
    for var in my_budget.income if len(my_budget.income[var])>0])

    expense_items = html.Div([
        html.Div([
            html.Div(" ",style = {'width': '5%'}),
            html.Div(var.title(), style = {'width': '15%'}),
            html.Div([
                html.Div([
                    html.Div(entry['description'], style = {'width':'65%', 'text-align': 'left'}),
                    html.Div("$" + str(entry['value']), style = {'width':'25%', 'text-align': 'left'}),
                    html.Button("E",id = {'type': 'edit_expenses', 'index': var +'__'+ str(idx)}),
                    html.Button("X",id = {'type': 'remove_expenses', 'index': var +'__'+ str(idx)}),
                ], style = {'display': 'flex'})
            for idx, entry in enumerate(my_budget.expenses[var])], style = {'width': '80%'})
        ], style = {'display': 'flex'})
    for var in my_budget.expenses if len(my_budget.expenses[var])>0])

    milestones =  html.Div([
        html.Div([
            html.Div(" ",style = {'width': '20%'}),
            html.Div([
                html.Div([
                    html.Div(entry['description']+" (" + entry['date'] + ")", style = {'width':'65%', 'text-align': 'left'}),
                    html.Div("$" + str(entry['value']), style = {'width':'25%', 'text-align': 'left'}),
                    html.Button("E",id = {'type': 'edit_milestones', 'index': 'milestone__' + str(idx)}),
                    html.Button("X",id = {'type': 'remove_milestones', 'index': 'milestone__' + str(idx)}),
                ], style = {'display': 'flex'})
            for idx, entry in enumerate(my_budget.milestones)], style = {'width': '80%'})
        ], style = {'display': 'flex'})
    ])

    return income_items, expense_items, milestones

# First callback is just to show the model and populate it with correct data
default_expense = budget_item('expenses','monthly',{'day': 1, 'value': 0, 'description': 'Add description here', 'category': 'add category tag here'})
default_income = budget_item('income','monthly',{'day': 1, 'value': 0, 'description': 'Add description here', 'category': 'add category tag here'})
default_milestone = budget_item('milestones',None,{'date': '12-25-2021', 'value': 0, 'description': 'Add description here', 'category': 'add category tag here'})

@app.callback(
    Output('budget_item_modal','is_open'),
    Output('modal_content', 'children'),
    Input({'type': 'edit_income', 'index': ALL}, 'n_clicks'),
    Input({'type': 'edit_expenses', 'index': ALL}, 'n_clicks'),
    Input({'type': 'edit_milestones', 'index': ALL}, 'n_clicks'),
    Input('add_income_button','n_clicks'),
    Input('add_expense_button','n_clicks'),
    Input('add_milestone_button','n_clicks'),
    Input('modal_cancel_button', 'n_clicks'),
    Input('modal_save_button','n_clicks'),
    State('budget_item_modal','is_open'),
    # State({'type': 'edit_income', 'index': ALL}, 'id'),
    State('main_budget','data'),
    prevent_initial_call=True
)
def open_modal(n0_1,n0_2, n0_3, n1,n2,n3,n4,n5,is_open,budget_data):
    ctx = dash.callback_context
    #print(ctx.triggered[0])
    if ctx.triggered[0]['prop_id'].split('.')[0][0] == '{':
        """ First, if the callback is trigged by the edit buttoms, make sure it's not on initial loading """
        if ctx.triggered[0]['value'] == None:
            print("This Worked")
            return False, None
        """ Start parsing the dictionary of ID to return the proper budget item"""
        id_dict = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        item_type = id_dict['type'][5:]
        item_idx = id_dict['index'].split('__')
        # print(item_idx[0], item_idx[1])
        # print(ctx.triggered[0]['prop_id'].split('.')[0], type(ctx.triggered[0]['prop_id'].split('.')[0]))
        # print(budget_data[item_type][item_idx[0]][int(item_idx[1])])
        if item_idx[0]=='milestone':
            loaded_item = budget_item(item_type, item_idx[0], budget_data[item_type][int(item_idx[1])])
        else:
            loaded_item = budget_item(item_type, item_idx[0], budget_data[item_type][item_idx[0]][int(item_idx[1])])
        return True, fill_modal(loaded_item,True)

    elif ctx.triggered[0]['prop_id'].split('.')[0] == 'add_expense_button':
        return True, fill_modal(default_expense)
    elif ctx.triggered[0]['prop_id'].split('.')[0] == 'add_income_button':
        return True, fill_modal(default_income)
    elif ctx.triggered[0]['prop_id'].split('.')[0] == 'add_milestone_button':
        return True, fill_modal(default_milestone)
    else:
        return False, None

# This callback happens when the modal drop-down for recurrence changes
@app.callback(
    Output('recurring_date_selector', 'children'),
    Input({"type": "modal_field", "index": 'modal_recurrence'},'value'),
    State({"type": "modal_cache", "index":'original_item_cached'}, 'data'),
    suppress_callback_exceptions = True,
    prevent_initial_call = True
)
def change_date_selectors(recurrence, cached_item):
    return day_selection_dropdowns(recurrence)

# This callback copies all the data from the modal entry fields and stores it in a dcc.Store location that doesn't reset when the modal closes
"""The reason for doing this is I can keep the Save/Cancel callbacks that close the modal clean in the open/close callback; 
    but I can also add callbacks to the Save button that actually add or modify the underlying Budget data
    To do this, I'll need the modal items to use a pattern-matching callback,
    that way I can set it up to fill a dictionary with a variable number of fields, and name them correctly
"""
@app.callback(
    Output('modal_fields_dump', 'data'),
    Input({'type': 'modal_field', 'index': ALL}, 'value'),
    State({'type': 'modal_field', 'index': ALL}, 'id'),
    State({'type': 'modal_cache', 'index': ALL}, 'data'),
    State({'type': 'modal_cache', 'index': ALL}, 'id'),
    State('modal_fields_dump', 'data'),
    State('budget_item_modal','is_open'),
    prevent_initial_call = True
)
def dump_fields(fields,ids,data, data_ids, old_dump, is_open):
    if is_open == False:
        return old_dump
    else:
        #Parse the indices from the dictionary of id's
        field_indices = [item['index'] for item in ids]
        data_indices = [item['index'] for item in data_ids]
        #use the indices to extract the fields we want from the modal entry form data that get's passed in
        edit_state = data[data_indices.index('edit_state')]
        old_data = data[data_indices.index('original_item_cached')]
        if old_data['type']=='income' or old_data['type']=='expenses':
            subtype = fields[field_indices.index('modal_recurrence')]
            fields.remove(subtype)
            field_indices.remove('modal_recurrence')
        else:
            subtype = None
        # This list-parsing here doesn't work; I need to expand this script a bit
        # item_dict = {field_indices[i]: fields[i] for i in range(len(fields))}
        item_dict = {}
        if old_data['type']=='income' or old_data['type']=='expenses':
            if subtype == 'monthly' or subtype == 'weekly':
                item_dict['day'] = fields[field_indices.index('modal_date')]
            elif subtype == 'one_off':
                item_dict['date'] = fields[field_indices.index('modal_date')]
        elif old_data['type']=='milestones':
            item_dict['date'] = fields[field_indices.index('modal_date')]
        item_dict['description'] = fields[field_indices.index('modal_description')]
        item_dict['value'] = fields[field_indices.index('modal_value')]        
        new_data = budget_item(old_data['type'],subtype,item_dict)
        # Wrap it all in a dict to store outside of the modal-content that's affected by the open/close callback
        output = {'edit_state': edit_state,
            'old_item': old_data,
            'new_item': new_data.__dict__
            }
        return output

# Add a callback to save the modal contents as a budget item
### This callback will need to get expanded to allow for uploading JSONs, and Editing JSONs
@app.callback(
    Output('main_budget','data'),
    Input('modal_save_button','n_clicks'),
    Input({'type': 'remove_income', 'index': ALL}, 'n_clicks'),
    Input({'type': 'remove_expenses', 'index': ALL}, 'n_clicks'),
    Input({'type': 'remove_milestones', 'index': ALL}, 'n_clicks'),
    Input('json_save_button','n_clicks'),
    State('main_budget','data'),
    State('modal_fields_dump','data'),
    State('json_edit_text','value'),
    prevent_initial_call = True,
)
def modify_budget(n0, n1_1, n1_2, n1_3, n2, budget, modal_dump, edit_json_text):
    ctx = dash.callback_context
    # First, for callback triggered by remove item buttons, find the item and remove it
    if ctx.triggered[0]['prop_id'].split('.')[0][0] == '{':
        """ First, if the callback is trigged by the remove buttoms, make sure it's not on initial loading """
        if ctx.triggered[0]['value'] == None:
            return (budget)
        else:
            """ Parse the dictionary to find the item to remove 
                This is copied code I don't need to replicate, so it's definitely an area I can improve"""
            id_dict = eval(ctx.triggered[0]['prop_id'].split('.')[0])
            item_type = id_dict['type'][7:]
            item_idx = id_dict['index'].split('__')
            if item_idx[0]=='milestone':
                loaded_item = budget_item(item_type, item_idx[0], budget[item_type][int(item_idx[1])])
            else:
                loaded_item = budget_item(item_type, item_idx[0], budget[item_type][item_idx[0]][int(item_idx[1])])
            my_budget = Budget(budget)
            my_budget.remove_item(loaded_item)
            return (my_budget.__dict__)
    # If the callback is triggered by the save button in the modal, run something else
    elif ctx.triggered[0]['prop_id'].split('.')[0] == 'modal_save_button':
        my_budget = Budget(budget)     
        new_item = budget_item(modal_dump['new_item']['type'],modal_dump['new_item']['subtype'],modal_dump['new_item']['item'])
        if modal_dump['edit_state']:
            old_item = budget_item(modal_dump['old_item']['type'],modal_dump['old_item']['subtype'],modal_dump['old_item']['item'])
            my_budget.remove_item(old_item)
        my_budget.add_item(new_item)
        return (my_budget.__dict__)
    # Next, if I save the json from text editor, overwrite the budget file (this could cause all kinds of bugs with text-errors, but this is a hobby project)
    elif ctx.triggered[0]['prop_id'].split('.')[0] == 'json_save_button':
        return (dict(json.loads(edit_json_text)))

# After these, we'll want to add one for uploading a scheme from JSON, and we'll want to add some fields for Starting Balance/Start Date

### Download budget as json ###
@app.callback(
    [Output(component_id= "json_dwnld", component_property = "data")],
    [Input("save_budget_button", "n_clicks",)],
    [State('main_budget','data')],
    prevent_initial_call = True,
    )
def download_data(n_clicks, budget):
    return [dcc.send_bytes(json.dumps(budget, indent = 4).encode('utf-8'), "MyBudget.json")]

### Edit JSON (show and close modal) ###
@app.callback(
    Output("json_modal","is_open"),
    Output("json_edit_text","value"),
    Input("edit_json_button","n_clicks"),
    Input("json_cancel_button","n_clicks"),
    Input("json_save_button","n_clicks"),
    State("main_budget","data"),
    prevent_initial_call = True
)
def show_json_editor(open,cancel,save,budget):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'].split('.')[0] == 'edit_json_button':
        return True, json.dumps(budget, indent = 4)
    else:
        return False, ""

### Tab 2 Callbacks ###

@app.callback(
    Output('forecast_graph','figure'),
    Output('slider_msgbox', 'children'),
    Input('main_budget','data'),
    Input('spending_slider', 'value')
    #Let's also add an input for the slider that changes monthly variable $
    )
def time_series_graph(data, spend):
    budget = Budget(from_json = data)
    fig, message = app_graphs.time_series_budget(budget, spend)
    return fig, message
