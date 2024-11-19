from dash import Dash, dcc, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Data
df = px.data.gapminder()

# Instantiate the App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App Layout
app.layout = dbc.Container([
    dcc.Markdown("# Befolkning i respektive länder"),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='länder',
                         options=[x for x in df.country.unique()],
                         multi=True,
                         value=['Canada', 'Brazil'])
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
    Input('länder', 'value')
)
def udpate_graph(countries_selected):
    df_filtered = df[df.country.isin(countries_selected)]
    fig = px.line(df_filtered, x='year', y='lifeExp', color='country')

    return fig

if __name__=='__main__':
    app.run_server(debug=True)