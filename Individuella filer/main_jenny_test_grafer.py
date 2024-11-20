import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import random

# Läs in din data
df = pd.read_csv("Project_Olympic/athlete_events.csv")

# Skapa en lista med unika sporter
sporter = df["Sport"].unique()

# Skapa en Dash-app
app = dash.Dash(__name__)

# Definiera appens layout
app.layout = html.Div([
    html.H1("Åldersfördelning i OS"),
    dcc.Dropdown(
        id="sport-dropdown",
        options=[{"label": sport, "value": sport} for sport in sporter],
        value=sporter[0]
    ),
    dcc.Graph(id="age-graph")
])

# Definiera en funktion som uppdaterar grafen när användaren väljer en ny sport
@app.callback(
    Output("age-graph", "figure"),
    [Input("sport-dropdown", "value")]
)
def update_graph(sport):
    # Filtrera data för den valda sporten
    df_sport = df[df["Sport"] == sport]
    df_sport = df_sport.dropna()

    # Skapar en hexadecimal färgkod och slumpar olika färger i grafen.
    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for _ in range(len(df_sport))]

    # Räknar antalet deltagare vid varje ålder.
    age_counts = df_sport[df_sport["Age"].notnull()]["Age"].value_counts().sort_index()
    # Skapa ett linjediagram för åldersfördelningen
    fig = px.line(x=age_counts.index, y=age_counts.values, title="Åldersfördelning i " + sport, labels={"x": "Ålder", "y": "Antal deltagare"}, color_discrete_sequence=colors)

    # Returnera grafen
    return fig

# Kör appen
if __name__ == "__main__":
    app.run_server()
