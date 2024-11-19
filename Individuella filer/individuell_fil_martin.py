import pandas as pd
import dash
from dash import dcc, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

# Läs in data från csv-filen
df = pd.read_csv("Project_Olympic/athlete_events.csv")

# Filtrera data för att bara inkludera Sommar OS
df_summer = df[df['Season'] == 'Summer']

# Gruppera data efter år och land, och räkna antalet deltagare
df_grouped = df_summer.groupby(["Year", "NOC"])["Name"].count().reset_index()

# Skapa en Dash-app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App-layout
app.layout = dbc.Container([
    dcc.Markdown("# Antalet deltagare i respektive land över tid (Sommar OS)"),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='country-dropdown',
                         options=[x for x in df_summer["NOC"].unique()],
                         multi=True,
                         value=['USA', 'SWE'])
        ], width=8)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='figure1')
        ], width=8)
    ])
])

# Configure Callback
@app.callback(
    Output('figure1', 'figure'),
    Input('country-dropdown', 'value')
)
def update_graph(countries_selected):
    df_filtered = df_grouped[df_grouped["NOC"].isin(countries_selected)]
    fig = px.line(df_filtered, x='Year', y='Name', color='NOC')
    fig.update_yaxes(title='Antal deltagare')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)