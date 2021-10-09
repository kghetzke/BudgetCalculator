import os
import glob
import pandas as pd
import json
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from application.app import app
from application.components.callbacks import callbacks
from application.components.datasteps.datasteps import Budget, budget_item
from application.components.layouts.tabs import tab1_layout, tab2_layout, tab3_layout
from application.components.layouts.modals import budget_item_entry_modal

### Header (for all tabs)###
basic_header = html.Div([
    html.Div(["Personal Budget App"], style = {'text-align': 'left', 'width': '100%'}),
    html.Div(["Click ",html.A("here",href='https://github.com/kghetzke/BudgetCalculator')," to view repository on GitHub"], style = {'text-align': 'right', 'width': '100%'})],
    style = {'display': 'flex'}
    )

### Tabs ###
tab_keys = dcc.Tabs(id = "tab_keys", value = "tab1", children = [
    dcc.Tab(label='Edit Budget', value = 'tab1', children = [tab1_layout()]),
    dcc.Tab(label='Forecast Savings', value = 'tab2', children = [tab2_layout()]),
    dcc.Tab(label='View Expense Allocations', value = 'tab3', children = [tab3_layout()]),  
])

content_container = html.Div(children=[], id = 'content_container')

### Footer ###
footer = html.Div(['This is a footer'], style = {'text-align': 'center'})

### Final Wrapper ###

with open('application\components\datasteps\\test_budget.json') as file:
    my_json = json.load(file)

def make_layout():
    layout = html.Div([
        dcc.Store(id = 'main_budget', data = my_json),
        dcc.Store(id = 'budget_alpha', data = None),
        dcc.Store(id = 'budget_beta', data = None),
        dcc.Store(id = 'budget_gamma', data = None),
        dcc.Store(id = 'budget_delta', data = None),
        budget_item_entry_modal(),
        basic_header,
        html.Br(),
        tab_keys,
        content_container,
        footer
    ])
    return layout
