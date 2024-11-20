# 1. Import packages
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import hashlib as hl

# Data imported here
file = pd.read_csv("Project_Olympic/athlete_events.csv")

# anonymisera kolumnerna med idrotternas namn
df = file.copy()
df["Name"] = df["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())

print(df)

# Initialise app
app = Dash(__name__)

# 2. Initialise the App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 3. Create app components
markdown = dcc.Markdown(id="our-markdown", children="My First Dash App", style={'textAlign': 'center', 'color': 'Pink', 'fontSize': 40})
# button = html.Button(children="Button")
# checklist = dcc.Checklist(options=['New York City', 'Montréal', 'San Francisco'])
# radio = dcc.RadioItems(options=['New York City', 'Montréal', 'San Francisco'])
dropdown = dcc.Dropdown(id="our-dropdown", options=['My first Dash app', 'Welcome to the app', 'This is the Title'], value='My first Dash app')
slider = dcc.Slider(id="our-slider", min=0, max=10, step=1, value=0)

# 4. App Layout
app.layout = dbc.Container(
    [
        dbc.Row([dbc.Col([markdown], width=8)]),
        dbc.Row([dbc.Col([dropdown], width=3)]),
    ]
)

# Callback
@app.callback(
    Output(component_id='our-markdown', component_property='children'),
    Input(component_id='our-dropdown', component_property='value')
)
def update_markdown(value_dropdown):
    title = value_dropdown
    return title

# 5. Run the App
if __name__ == '__main__':
    app.run_server()


