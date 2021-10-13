# BudgetCalculator
An easy GUI to create a savings plan

### Project Notes:
1. Build a datasteps.py script that defines a class Budget() that is basically just a dictionary of items in someones budget that I'll want to use in the app (date-range, starting balance, recurring income and expenses, etc.).  If this class can initialize itself from a json dictionary, contain methods to parse itself into a dataframe for plots and other anlysis, and contain methods to add, remove, and modify parameters in the dictionary, I should have everything I need to build a GUI on top of this in Dash. I can add methods here for fancier data manipulations if I want to later.
2. Build a graphs.py script that takes data from a Budget() object and generates all the plots I'd want to display.  These functions will return figures that can be rendered in a Dash layout.
3. Use a standard Dash file structure to define app.py, index.py, layout.py, and callbacks.py.  The layout will be structured as follows: 
    -First, a dcc.Store() object will be used to save the parameters of Budget() in a small json-style dictionary.  
    -Second, there will be a header with some tabs; the multi-tab structure will be built out to add any new layers of analysis, graphs will appear in each tab with dynamic objects (dropdowns, buttons, etc.) that users can use to manipulate graphs. 
        -The primary tab will display a line-chart with Cash-Balance over time, and certain milestone dates marked.  It will have simple dropdowns for changing start date, end date, and initial balance; it will also have buttons for "Add Expense", "Add Income", and "Add Milestone" that launch simple entry forms to pass parameters into the add() method of Budget().   
        -A secondary tab will show lists of all income, expenses, and milestone entries, and this tab will contain more buttons to prompt entry-forms for the user to modify entries, remove entries, or add entries.
        -I'd like a third tab to show pie-charts breaking down monthly, weekly, and daily expenses by category, and maybe a button that toggles the inclusion of all expenses (ex. the "monthly expenses" pie chart can show total of all expenses for the month, or only expenses that recur at a monthly level)
4. I need to think carefully about how to structure callbacks. The Budget() object in dcc.Store() can only be modified in a single callback; i.e. I can't have multiple callbacks outputing data to the same dcc.Store() object.
5. I would love to have a method for uploading, editing, and downloading a Budget() object as a json file.  I know how to do download without issue; I haven't use upload, and it would be really cool to have a built-in json editor that the user can use in conjunction with the GUI buttons to make modifications to their budget.
6. If I get really fancy, I can work out a way to cache budget data for each user so they can return to their dashboard in a later session without having to download and re-upload the json file.


#### Scrum Cards...
- [COMPLETED] Create and clone a repository on GitHub, and establish a working folder structure for this project
- [COMPLETED] Create a JSON dictionary with items I would want to track for my own budget.
- [COMPLETED] Build a Budget class around the JSON dictionary
- [COMPLETED] Add an init method to the Budget class to initialize itself from json
- [COMPLETED] Add a parse_df() method to Budget class to take budget items and serialize them as a cash-balance over time
- [COMPLETED] Create a first-draft of a graphs.py file that has a function to take the Budget class and return a line-chart as a plotly-fig showing cash over time
- [COMPLETED] Add app.py and index.py to run and test a dash app
- [COMPLETED] create a basic layout.py file to include a header, tabs, content containers, and a footer; wrap everything in a make_layout() function so the index.py script runs properly
- [COMPLETED] create a basic callbacks.py file and add a single callback to switch between tabs -> while completing this card I realized I needed to add a tabs.py file to prevent circular imports so that the layouts.py file can import callbacks, but the callbacks can return layout-type objects when the callback to switch tabs is called
- [COMPLETED] add some layout features for Tab2 and a callback to callbacks.py that displays a graph using the function in graphs.py
- [COMPLETED] create a basic layout for Tab1, and add callbacks that dynamically fill in rows of text for each budget entry, and buttons that we will use to edit or remove a budget item
- [COMPLETED] Work out how to launch an entry form using dcc.Modal when a button is clicked. I'd like the add and edit buttons in tab-1 to launch entry forms where users can fill out simple fields to add/edit budget items. [UPDATE]: I have a functionning modal that displays, but I want to recycle the same "show modal" callback for different content based on what modal is clicked, and how I can pipe-in values to the entry form based on selection.
- [COMPLETED] Work out how the dynamically generated buttons can be associated with the items in the budget they are rendered next to.  I want the remove-item button to remove a specific item (the one in line next to it), but to do this I need to figure out how to connect the dynamically generated button to the specific item it's generated next to
- [COMPLETED] Modify my graph function to display cash-flow based on an additional argument for variable-spending;
- I'd like to work out a simple optimization tool to "optimize" savings based on milestones - calculate the minimum savings required per month to reach your various savings milestones
- [COMPLETED]Add a callback to get the download-current-budget button to work (simple download method I've used before)
- Add a callback to get the "upload budget schema" button to work (theoretically simple with dcc.Upload, but I haven't used this before)
- [COMPLETED] Determine if it's worth adding a built-in JSON editor to allow users to modify the JSON from browser; I think I can get the text-editor to work, but I don't think I can get the app to run in a forgiving way, where syntax errors are ignored rather than breaking the entire project. [UPDATE] - I didn't really build out a full editor; just use a Textarea input box to render the json-style layout of the current budget, that users can then make modifications to. If this were a real app launch, this feature would offer a very unforgiving user experience, as there are no built-in error checks. But, as a proof-of-concept/hobby project, I'm pleased with this much effort.
- Learn more about CSS styling and add a styles.css file to this app so that it doesn't look so bare
- Add some content to Tab3; I'm thinking basic pie-charts that just show income / expense allocations, so these pie charts should be done after a quick session.
- [COMPLETED] Modify the layout of Tab2 and add a callback so the slider calculates allows users to select a percentage of disposable income to spend each month from 0-200%. 
- Deploy the app to Heroku, and link on my resume
- Do some comsmetic adjustments to all graphs and visualizations (no default labeling, etc.)