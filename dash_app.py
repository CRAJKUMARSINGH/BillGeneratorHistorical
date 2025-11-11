import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Create a sample dataset
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    
    dcc.Graph(
        id='example-graph',
        figure=px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    )
])

# Run the server
if __name__ == '__main__':
    app.run(debug=True, port=8050)