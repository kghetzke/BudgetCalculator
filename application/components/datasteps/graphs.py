import pandas as pd
import plotly.express as px

from application.components.datasteps.datasteps import Budget

def dollars_rounding(i):
    """ Take a numeric value less than 1 billion, and return a rounded string, like $15K, or $10.2K """
    if i<1000:
        return "$" + str(int(i))
    elif i>=1000 & i<1000000:
        if i % 1000==0:
            return "$" + str(int(i/1000)) + "k"
        else:
            return "$" + str(round(i/1000,1)) + "k"
    elif i>=1000000 & i<1000000000:
        if i % 1000000==0:
            return "$" + str(int(i/1000000)) + "M"
        else:
            return "$" + str(round(i/1000000,1)) + "M"
    else:
        return

def time_series_budget(budget: Budget, avg_spending):
    """ Creates a Time-Series Plot of the budget"""
    data = budget.parse_df()
    data['CashBalance'] = budget.starting_balance + (data['Income']-data['Expenses']-(avg_spending/30.4)).cumsum()

    fig = px.line(data, y="CashBalance")

    for obj in budget.milestones:
        date = pd.to_datetime(obj['date'])
        fig.add_vline(x=date)
        fig.add_annotation(x=date,y=obj['value'],text=obj['description'], showarrow=True, xanchor='right',hovertext = "Savings target of " + dollars_rounding(obj['value']))
    return fig



# Some code to test these functions
if __name__=='__main__':
    import json
    with open('application\components\datasteps\\my_budget.json') as file:
        my_json = json.load(file)
    my_budget = Budget(from_json=my_json)

    # First figure.
    fig = time_series_budget(my_budget, 500)
    fig.write_html('test_files\\plot_test1.html',auto_open = True)