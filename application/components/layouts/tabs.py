import os
import glob
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

### Tab 1 Content ###
tab1_head = html.H1(['My Budget Items'],style = {'width': '100%', 'text-align': 'center'})

main_buttons = html.Div([
    html.Button("Upload Budget Schema", id="upload_budget_button", style = {'width': '30%', 'margin':'auto'}),
    html.Button("Edit JSON", id = "edit_json_button", style = {'width': '30%', 'margin': 'auto'}),
    html.Button("Download Current Schema", id = "save_budget_button", style = {'width': '30%', 'margin': 'auto'})],
    style = {'display':'flex', 'width': '40%', 'margin': 'auto'}
    )

income_items = html.Div([
    html.H3(['Fixed Income Sources']),
    html.Div(children=[],id="income_items_container"),
    html.Div([
        html.Div(" ",style = {'width': '20%'}),
        html.Button("Add Income Item", id="add_income_button")
    ], style = {'display': 'flex'})
])

expense_items = html.Div([
    html.H3(['Fixed Expenses']),
    html.Div(children=[],id="expense_items_container"),
    html.Div([
        html.Div(" ", style={'width': '20%'}),
        html.Button("Add Fixed Expense ", id="add_expense_button")
    ], style = {'display': 'flex'})
])

milestone_items = html.Div([
    html.H3(['Savings Milestones']),
    html.Div(children=[],id="milestones_container"),
    html.Div([
        html.Div(" ", style={'width': '20%'}),
        html.Button("Add Milestone", id="add_milestone_button")
    ], style = {'display': 'flex'})
])

def tab1_layout():
    layout = html.Div([
        tab1_head,
        html.Hr(style = {'width': '35%'}),
        main_buttons,
        html.Hr(),
        income_items,
        expense_items,
        milestone_items,
        html.Hr()
    ])
    return layout

### Tab 2 Content ###
tab2_head = html.Div(['This is Tab 2'])

def tab2_layout():
    layout = html.Div([
        tab2_head,
        dcc.Graph(id = "forecast_graph", figure = {}),
        html.Div([
            html.Div("Manually set spending (as % of disposable income)", style = {'margin': 'auto', 'text-align': 'center'}),
            dcc.Slider(id = "spending_slider", min=0, max=200, value=50, marks ={0: '0%', 100: '100%', 200: '200%'})
            ],
            id = 'slider_container',
            style = {'width': '35%', 'margin': 'auto'}
        ),
        html.Div([html.Button('Optimize Spending', id='optimize_spend_button')], style={'width': '30%', 'margin': 'auto'}),
        html.Hr()
    ])
    return layout


### Tab 3 Content ###
tab3_head = html.Div(['This is Tab 3'])

def tab3_layout():
    layout = html.Div([
        tab3_head
    ])
    return layout