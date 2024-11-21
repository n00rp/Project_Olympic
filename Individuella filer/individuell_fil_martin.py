#Fungerande version! 

import pandas as pd
import dash
from dash import dcc, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

# Läs in data från csv-filen
df = pd.read_csv("../athlete_events.csv")

# Skapa en lista med unika sporter
sports = df['Sport'].unique()

# Skapa en Dash-app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# App-layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Tabs(id='tabs', value='tab-2', children=[
                dcc.Tab(label='Antalet deltagare i respektive land och sport över tid (Sommar OS)', value='tab-2'),
                dcc.Tab(label='Antalet deltagare i respektive land och sport över tid (Vinter OS)', value='tab-3')
            ])
        ], width=2),  # vänster kolumn
        dbc.Col([
            html.Div(id='tabs-content', children=[
                html.Div(id='tab-2-content', children=[
                    dcc.Dropdown(id='country-dropdown-2',
                                 options=[x for x in df['NOC'].unique()],
                                 multi=True,
                                 value=['USA', 'SWE']),
                    dcc.Dropdown(id='sport-dropdown',
                                 options=[{'label': sport, 'value': sport} for sport in sports],
                                 multi=True,
                                 value=['Athletics', 'Swimming']),
                    dcc.Graph(id='figure2'),
                    dcc.Graph(id='figure-medals')
                ]),
                html.Div(id='tab-3-content', children=[
                    dcc.Dropdown(id='country-dropdown-3',
                                 options=[x for x in df['NOC'].unique()],
                                 multi=True,
                                 value=['USA', 'SWE']),
                    dcc.Dropdown(id='sport-dropdown-3',
                                 options=[{'label': sport, 'value': sport} for sport in sports],
                                 multi=True,
                                 value=['Alpine Skiing', 'Figure Skating']),
                    dcc.Graph(id='figure3'),
                    dcc.Graph(id='figure-medals-3')
                ])
            ])
        ], width=10)  # höger kolumn
    ])
])



# Configure Callback
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return tab_1_layout
    elif tab == 'tab-2':
        return html.Div(id='tab-2-content', children=[
            dcc.Dropdown(id='country-dropdown-2',
                         options=[x for x in df['NOC'].unique()],
                         multi=True,
                         value=['USA', 'SWE']),
            dcc.Dropdown(id='sport-dropdown',
                         options=[{'label': sport, 'value': sport} for sport in sports],
                         multi=True,
                         value=['Athletics', 'Swimming']),
            dcc.Graph(id='figure2'),
            dcc.Graph(id='figure-medals')
        ])
    elif tab == 'tab-3':
        return html.Div(id='tab-3-content', children=[
            dcc.Dropdown(id='country-dropdown-3',
                         options=[x for x in df['NOC'].unique()],
                         multi=True,
                         value=['USA', 'SWE']),
            dcc.Dropdown(id='sport-dropdown-3',
                         options=[{'label': sport, 'value': sport} for sport in sports],
                         multi=True,
                         value=['Alpine Skiing', 'Figure Skating']),
            dcc.Graph(id='figure3'),
            dcc.Graph(id='figure-medals-3')
        ])
    elif tab == 'tab-4':
        return html.Div(id='tab-4-content', children=[
            dcc.Dropdown(id='country-dropdown-4',
                         options=[x for x in df['NOC'].unique()],
                         multi=True,
                         value=['USA', 'SWE']),
            dcc.Graph(id='figure4')
        ])

@app.callback(
    Output('figure1', 'figure'),
    Input('country-dropdown-2', 'value')
)
def update_graph(countries_selected):
    df_filtered = df[df['NOC'].isin(countries_selected)]
    df_filtered = df_filtered[df_filtered['Season'] == 'Summer']
    df_counts = df_filtered.groupby(['Year', 'NOC'])['ID'].count().reset_index()
    df_counts.columns = ['Year', 'Land', 'Antal deltagare']
    fig = px.line(df_counts, x='Year', y='Antal deltagare', color='Land')
    fig.update_yaxes(title='Antal deltagare')
    return fig

@app.callback(
    Output('figure2', 'figure'),
    Input('country-dropdown-2', 'value'),
    Input('sport-dropdown', 'value')
)
def update_graph(country_selected, sports_selected):
    df_filtered = df[(df['NOC'].isin(country_selected)) & (df['Sport'].isin(sports_selected))]
    df_counts = df_filtered.groupby(['Year', 'Sport'])['NOC'].count().reset_index()
    df_counts.columns = ['Year', 'Sport', 'Antal deltagare']
    fig = px.line(df_counts, x='Year', y='Antal deltagare', color='Sport')
    fig.update_yaxes(title='Antal deltagare')
    return fig


@app.callback(
    Output('figure-medals', 'figure'),
    Input('country-dropdown-2', 'value'),
    Input('sport-dropdown', 'value')
)
def update_medals(country_selected, sports_selected):
    df_filtered = df[(df['NOC'].isin(country_selected)) & (df['Sport'].isin(sports_selected))]
    df_medals = df_filtered[df_filtered['Medal'].notna()]
    df_medals = df_medals.groupby(['Sport', 'Medal'])['NOC'].count().reset_index()
    df_medals.columns = ['Sport', 'Medal', 'Antal medaljer']
    fig = px.pie(df_medals, values='Antal medaljer', names='Medal')
    fig.update_layout(title='Antalet medaljer i valda sporterna')
    return fig
@app.callback(
    Output('figure3', 'figure'),
    Input('country-dropdown-3', 'value'),
    Input('sport-dropdown-3', 'value')
)
def update_graph(country_selected, sports_selected):
    df_filtered = df[(df['NOC'].isin(country_selected)) & (df['Sport'].isin(sports_selected)) & (df['Season'] == 'Winter')]
    df_counts = df_filtered.groupby(['Year', 'Sport'])['NOC'].count().reset_index()
    df_counts.columns = ['Year', 'Sport', 'Antal deltagare']
    fig = px.line(df_counts, x='Year', y='Antal deltagare', color='Sport')
    fig.update_yaxes(title='Antal deltagare')
    return fig

@app.callback(
    Output('figure-medals-3', 'figure'),
    Input('country-dropdown-3', 'value'),
    Input('sport-dropdown-3', 'value')
)
def update_medals(country_selected, sports_selected):
    df_filtered = df[(df['NOC'].isin(country_selected)) & (df['Sport'].isin(sports_selected)) & (df['Season'] == 'Winter')]
    df_medals = df_filtered[df_filtered['Medal'].notna()]
    df_medals = df_medals.groupby(['Sport', 'Medal'])['NOC'].count().reset_index()
    df_medals.columns = ['Sport', 'Medal', 'Antal medaljer']
    fig = px.pie(df_medals, values='Antal medaljer', names='Medal')
    fig.update_layout(title='Antalet medaljer i valda sporterna')
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)