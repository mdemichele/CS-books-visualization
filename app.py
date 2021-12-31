import dash 
from dash import dcc 
from dash import html 
from dash import dash_table
from dash.dependencies import Input, Output
import pandas as pd 

app = dash.Dash(__name__)

# Read in our books data 
df = pd.read_csv('./prog_book.csv')

# Create table columns 
table_columns = df[["Rating", "Reviews", "Book_title", "Number_Of_Pages", "Type", "Price"]]

app.layout = html.Div([
    # Create our dropdown menu 
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Rating', 'value': 'Rating'},
            {'label': 'Pages', 'value': 'Number_Of_Pages'},
            {'label': 'Price', 'value': 'Price'}
        ],
        value='Rating'
    ),
    
    # Create our Graph 
    dcc.Graph(
        id='my-graph',
    ),
    
    html.Div(
        dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in table_columns],
            data=df.to_dict('records'),
            page_size=10)
    )
])

# Create our graph 
@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='my-dropdown', component_property='value'))
def update_graph(value):
    
    # get the column is referenced by the dropdown (i.e. rating, number_of_pages, price) 
    selected_columns = df[["Book_title", value]]
    
    # Sort in descending order 
    sorted_columns = selected_columns.sort_values(by=value, ascending=False)
    
    # Cut down to top 10
    truncated = sorted_columns.iloc[0:10]
    
    return {
    'data': [
        {'y': truncated["Book_title"], 'x': truncated[value], 'type': 'bar', 'orientation': 'h', 'name': df.Book_title}, 
    ],
    'layout': {
        'margin': {'l': 550, 'r': 30, 't': 50, 'b': 50},
        'title': {'text': 'Top 270 Computer Science / Programming Books'},
    },
    }
    
    

if __name__ == '__main__':
    app.run_server(debug=True)