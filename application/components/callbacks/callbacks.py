import io
import json
from datetime import datetime
import pandas as pd
import plotly.express as px

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, ALL

from application.app import app
from application.components.layouts.tabs import tab1_layout, tab2_layout, tab3_layout
import  application.components.datasteps.graphs as app_graphs
from application.components.datasteps.datasteps import Budget, budget_item

"""
### First Callback: Switch between Tabs ###

@app.callback(
    Output('content_container','children'),
    Input(component_id="tab_keys", component_property = "value")
    )
def choose_tab(tab):
    if tab=='tab1':
        return tab1_layout()
    elif tab=='tab2':
        return tab2_layout()
    elif tab=='tab3':
        return tab3_layout()
"""
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
                    html.Button("E",id = {'type': 'edit_income_'+var, 'index': idx}),
                    html.Button("X",id = {'type': 'remove_income_'+var, 'index': idx}),
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
                    html.Button("E",id = {'type': 'gamma', 'index': idx}),
                    html.Button("X",id = {'type': 'delta', 'index': idx}),
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
                    html.Button("E",id = {'type': 'epsilon', 'index': idx}),
                    html.Button("X",id = {'type': 'zeta', 'index': idx}),
                ], style = {'display': 'flex'})
            for idx, entry in enumerate(my_budget.milestones)], style = {'width': '80%'})
        ], style = {'display': 'flex'})
    ])

    return income_items, expense_items, milestones

# To keep the budget-editing code a little cleaner, I'm going to separate the callbacks for the different ways budget can be edited
# For this to work, I first need a callback that updates the main budget whenever data changes in the other spots
"""
@app.callback(
    Output('main_budget','data'),
    Input('budget_alpha','data'),
    Input('budget_beta','data'),
    Input('budget_gamma','data'),
    Input('budget_delta','data')
)
def update_budget(alpha, beta, gamma, delta):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'].split('.')[0] == 'budget_alpha':
        return alpha
    else:
        pass
"""
# simple test here. In the add-milestone callback, let's add something simple and save it to main budget
@app.callback(
    Output('main_budget','data'),
    Input('add_milestone_button','n_clicks'),
    State('main_budget','data'),
    prevent_initial_call = True,
)
def add_budget_item(n, budget):
    my_budget = Budget(budget)
    my_budget.add_item(budget_item('milestone',None,{'date': '12-25-2022', 'description': 'Christmas Day', 'value': 500}))
    return (my_budget.__dict__)



### Tab 2 Callbacks ###

@app.callback(
    Output('forecast_graph','figure'),
    Input('main_budget','data'),
    Input('spending_slider', 'value')
    #Let's also add an input for the slider that changes monthly variable $
    )
def time_series_graph(data, spend):
    budget = Budget(from_json = data)
    return app_graphs.time_series_budget(budget, spend)
