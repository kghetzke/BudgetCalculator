"""
This "datasteps" code defines a class called budget, and this class has some methods to add to it, and save's itself in a json format
"""
import json
import pandas as pd
import numpy as np
from dataclasses import dataclass
from enum import Enum

# First, I want to create a simple dataclass for budget items
@dataclass
class budget_item:
    type: str
    subtype: str
    item: dict


# The main class of objects I'll be using here is a class for a budget; 
# which is really just a dictionary of recurring expenses and income, with some built in methods for parsing
class Budget:
    def __init__(self, from_json=None):
        if from_json==None:
            """Initialize with some default values"""
            self.start_date = '09-23-2021'
            self.end_date = '09-23-2022'
            self.starting_balance = 0.00
            self.income = {'monthly': [], 'weekly': [], 'daily': [], 'one_off':[]}
            self.expenses = {'monthly': [], 'weekly': [], 'daily': [], 'one_off':[]}
            self.milestones = []
        else:
            """Parse a Json-dictionary and assign all the values"""
            self.start_date = from_json['start_date']
            self.end_date = from_json['end_date']
            self.starting_balance = from_json['starting_balance']
            self.income = from_json['income']
            self.expenses = from_json['expenses']
            self.milestones = from_json['milestones']
            pass
    
    def add_item(self,new_item: budget_item):
        if new_item.type=='income':
            self.income[new_item.subtype].append(new_item.item)
        elif new_item.type=='expenses':
            self.expenses[new_item.subtype].append(new_item.item)
        elif new_item.type=='milestones':
            self.milestones.append(new_item.item)

    def remove_item(self, item: budget_item):
        if item.type=='income':
            self.income[item.subtype].remove(item.item)
        elif item.type=='expenses':
            self.expenses[item.subtype].remove(item.item)
        elif item.type=='milestones':
            self.milestones.remove(item.item)

    def modify_item(self, org_item: budget_item, new_item: budget_item):
        self.remove_item(org_item)
        self.add_item(new_item)

    def parse_df(self):
        """ This method uses the budget object to create a pandas-dataframe of time-series income/expenses """
        # Create an empty dataframe of the proper lenght, indexed with days
        days = pd.date_range(self.start_date, self.end_date)
        df = pd.DataFrame(np.zeros((len(days),2)), index=days, columns = ['Income','Expenses'])

        # Sum up income and expenses in the Income and Expense columns
        for column in [self.income, self.expenses]:
            if column==self.income: 
                var='Income' 
            else: 
                var='Expenses'
            for obj in column['monthly']:
                if obj['day']=='last':
                    df[var][np.roll(df.index.day==1,-1)] = df[var][np.roll(df.index.day==1,-1)] +  obj['value']
                else:
                    df[var][df.index.day==obj['day']]=df[var][df.index.day==obj['day']] + obj['value']
            for obj in column['weekly']:
                df[var][df.index.day_name()==obj['day']]=df[var][df.index.day_name()==obj['day']] + obj['value']
            for obj in column['daily']: 
                df[var] = df[var] + obj['value']
            for obj in column['one_off']:
                df[var][df.index==obj['date']] = df[var][df.index==obj['date']] + obj['value']

        # Create a cumulative sum column
        df['CashBalance'] = self.starting_balance + (df['Income']-df['Expenses']).cumsum()

        # Add milestone notes to certain days we'll want to highlight with the Milestones objects
        df['Milestones'] = np.nan
        for milestone in self.milestones:
            df['Milestones'][milestone['date']]=milestone['description']

        return df
    def expense_df(self):
        """ This Method Returns a Dataframe of all expense entries"""
        # First, get all the expenses in one dataframe
        df = pd.DataFrame(data=None,columns = ['Recurrence','Value','Description','Category'])
        for period in ['monthly','weekly','daily']:
            for obj in self.expenses[period]:
                new_row = pd.DataFrame([period,obj['value'],obj['description'],obj['category']],index = ['Recurrence','Value','Description','Category']).transpose()
                df = df.append(new_row)
        df = df.reset_index(drop=True)

        # Second, do some math so they're normalized with each other
        
        return df



# Here's some simple code just to test what I'm doing here

if __name__=='__main__':
    """Test that I can load a JSON containing budget data, and properly parse that data as a data-frame"""
    with open('application\components\datasteps\\test_budget.json') as file:
        my_json = json.load(file)
    my_budget = Budget(from_json=my_json)
    print(my_budget.__dict__)
    df = my_budget.parse_df()
    print(df.head())
    df.to_csv('test_files\\test.csv')

    alt_df = my_budget.expense_df()
    print(alt_df)

    """ Next, test that I can add and remove items correctly with my modification functions"""
    test_item = budget_item('milestone',None,{'date': '12-25-2022', 'description': 'Christmas Day'})
    print(my_budget.milestones)
    my_budget.add_item(test_item)
    print(my_budget.milestones)
    my_budget.remove_item(test_item)
    print(my_budget.milestones)

    test_item_2 = budget_item('income','weekly',{'value': 50, 'day': 'Friday','description':'Test Income'})
    print(my_budget.income)
    my_budget.add_item(test_item_2)
    print(my_budget.income)

    """ I'm having some issues with callbacks, so test that I can save the class as dict and re-initialize it"""
    print(my_budget.milestones)
    budget_dict = my_budget.__dict__
    budget_reinit = Budget(budget_dict)
    print(budget_reinit.milestones)