from dash import Dash, dcc, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Läs in data
df = pd.read_csv("../athlete_events.csv")

# Instantiate the App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App Layout
app.layout = dbc.Container([
    dcc.Markdown("Åldersfördelning i respektive sport"),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='sport',
                         options=[x for x in ["Sailing", "Curling", "Football", "Handball"]],
                         multi=True,
                         value=['Curling', 'Handball'])
        ], width=8)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='figure1')
        ], width = 8)
    ])
])


# Configure Callback
@app.callback(
    Output('figure1','figure'),
    Input('sport', 'value')
)
def udpate_graph(sport_selected):
    df_filtered = df[df.Sport.isin(sport_selected)]
    fig = px.histogram(df_filtered, x='Age', color='Sport', opacity=.4, range_x=[10,70], range_y=[0,1000], barmode="overlay")

    return fig

if __name__=='__main__':
    app.run_server(debug=True)