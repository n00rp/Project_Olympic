import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, State, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
#--------------------------------------------------------------------------------------------------------------
df = pd.read_csv("Project_Olympic/athlete_events.csv")

""" Tabell på antal medaljer per individ i tyskland """
ger_df = df[df["NOC"] == "GER"]
medal = ger_df["Medal"].isin(["Gold", "Silver", "Bronze"])
medals = ger_df[medal]
color1 = ["silver", "orange", "gold"]

""" Tabell på medaljer som nation i Tyskland """
temp_df = ger_df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
ny_team_variabel = temp_df["Medal"].isin(["Gold", "Silver", "Bronze"])
ny_team_variabel = temp_df[ny_team_variabel]

""" Tabell på medaljer """
ny_team_variabel["Medaltot"] = 1
df_grouped = ny_team_variabel.groupby(['Year', 'Medal']).sum().reset_index()
df_pivot = df_grouped.pivot(index='Year', columns='Medal', values='Medaltot')# Pivot = Year blir x-axeln och Medal blir kolumner med en valör i varje. Values(Medeltot) får summan av varje valör per år.
df_pivot_g = df_pivot["Gold"]
df_pivot_s = df_pivot["Silver"]
df_pivot_b = df_pivot["Bronze"]

#----------------------------------------------------------------------------------------------------------------

def medalj_individ():
    fig = px.bar(medals, x="Medal", color="Medal", color_discrete_sequence=color1, width=550, height=650)
    fig.update_layout(title="Tyska Individuella Medaljer", xaxis_title="Valör", yaxis_title="Antal")
    return dcc.Graph(id="medalj_individ", figure=fig)

def medalj_nation():
    fig = px.bar(ny_team_variabel, x="Medal", color="Medal", color_discrete_sequence=color1, width=550, height=650)
    fig.update_layout(title="Tyska Nationella Medaljer", xaxis_title="Valör", yaxis_title="Antal")
    return dcc.Graph(id="medalj_nation", figure=fig)

#------------------------------------------------------------------------------------------------------------------

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([

    dbc.Card(
        dbc.CardBody([
            html.H2("Välkommen till Olympiska Spelen!", className="card-title"),
            html.P("Utforska medaljdata för Tyskland och andra nationer i de Olympiska spelen.", className="card-text"),
            html.Img(src='/assets/os_ringar.png', style={'width': '15%', 'display': 'block', 'margin': '0 auto'}),
        ]),
        className="mb-4 border-primary",  # Border och marginal
        style={"margin-top": "20px", "textAlign": "center"}
    ),

    # Rubrik för OLYMPISKA SPELEN
    html.H1("OLYMPISKA SPELEN", style={"textAlign": "center", "color": "blue"}),

    # Horisontell linje
    html.Hr(),

    # Rubrik för nästa sektion
    html.H1("TYSKLAND", style={"textAlign": "center", "color": "black"}),

    # Flexbox container för vänster och höger card
    dbc.Row([
        # Stort Card till vänster (8/12 bredd)
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H4("Tyska Medaljer", className="card-title"),
                    dcc.Tabs([
                        dcc.Tab(label="Individuella medaljer", children=[medalj_individ()], style={'padding': '20px'}),
                        dcc.Tab(label="Nationella medaljer", children=[medalj_nation()], style={'padding': '20px'})
                    ])
                ]),
                className="mb-3", style={"max-width": "100%", "margin": "0 auto"}
            ),
            width=4  # 8 delar av en 12-kolumn layout för stort card
        ),


        dbc.Col(
            children=[
                dbc.Card(
                    dbc.CardBody([
                        html.Div(
                            className="d-flex align-items-center",
                            children=[
                                html.Img(src='/assets/guld.png', style={'width': '15%', 'margin-right': '10px'}),  # Bild till vänster
                                html.Div([
                                    html.H4("745", className="card-text"),
                                    html.P("Guld medaljer", className="card-text")
                                ])
                            ]
                        ),
                    ]),
                    className="mb-3", style={"height": "150px", "margin": "0"}
                ),

                dbc.Card(
                    dbc.CardBody([
                        html.Div(
                            className="d-flex align-items-center",
                            children=[
                                html.Img(src='/assets/silver.png', style={'width': '15%', 'margin-right': '10px'}),  # Bild till vänster
                                html.Div([
                                    html.H4("674", className="card-text"),
                                    html.P("Silver medaljer", className="card-text")
                                ])
                            ]
                        ),
                    ]),
                    className="mb-3", style={"height": "150px", "margin": "0"}
                ),

                dbc.Card(
                    dbc.CardBody([
                        html.Div(
                            className="d-flex align-items-center",
                            children=[
                                html.Img(src='/assets/bronz.png', style={'width': '18%', 'margin-right': '10px'}),  # Bild till vänster
                                html.Div([
                                    html.H4("746", className="card-text"),
                                    html.P("Brons medaljer", className="card-text")
                                ])
                            ]
                        ),
                    ]),
                    className="mb-3", style={"height": "150px", "margin": "0"}
                )
            ],
            width=2  # 4 delar av en 12-kolumn layout för den högerkolumnen med små cards
        ),# Kolumnen stängs här

        dbc.Col(
        children=[
            # Card med tabellen
            dbc.Card(
                dbc.CardBody([
                    html.H4("Tysklands OS städer", style={"textAlign": "center"}),
                    dash_table.DataTable(
                        columns=[
                            {"name": "Stad", "id": "stad"},
                            {"name": "Typ av OS", "id": "os_type"},
                            {"name": "År", "id": "year"}
                        ],
                        data=[
                            {"stad": "Berlin", "os_type": "Sommar OS", "year": "1916 (Inställt)"},
                            {"stad": "Berlin", "os_type": "Sommar OS", "year": "1936"},
                            {"stad": "Garmisch-Partenkirchen", "os_type": "Vinter OS", "year": "1936"},
                        ],
                        style_table={'width': '100%', 'margin': '0 auto'},
                        style_header={'backgroundColor': 'lightblue', 'fontWeight': 'bold'},
                        style_cell={'textAlign': 'center', 'padding': '10px'},
                    )
                ]),
                className="mb-3", style={"height": "auto", "width": "100%"}  # Flexibelt kort för tabellen
            ),
            dbc.Card(
                dbc.CardBody([
                    dcc.Dropdown(options=[
                            {"label": "Gold", "value": "Gold"},
                            {"label": "Silver", "value": "Silver"},
                            {"label": "Bronze", "value": "Bronze"}
                        ],  value= "Gold", id="dropdown-item"
                    ),
                    dcc.Graph(id="dd_graph")
                ])
            )
        ]
        )
        #skriv en ny kolumn här


    ]),# Raden stängs här

    dbc.Row([
        dbc.Col([
            dbc.Card(
                    dbc.CardBody([
                        dcc.Dropdown(options=[
                                    {"label": "Man", "value": "Man"},
                                    {"label": "Kvinna", "value": "Kvinna"},
                                ],  value= "Man", id="dropdown-gender-output"
                        ),
                        dcc.Graph(id="dd_gender_graph")
                    ]),
                    className="mb-3", style={"width": "100%"}  # Flexibelt kort för dropdownen
                )  
        ],width=6  # 3 delar av en 12-kolumn layout för tabellen och dropdown
        ),
        dbc.Col([
            dbc.Card(
                    dbc.CardBody([
                        dcc.Dropdown(options=[
                                    {"label": "Sommar", "value": "Sommar"},
                                    {"label": "Vinter", "value": "Vinter"},
                                ],  value= "Man", id="dropdown-gender"
                        ),
                        html.Div(id="dropdown-season_emil"),
                        dcc.Graph(id="emil_top_sports")
                    ]),
                    className="mb-3", style={"width": "100%"}  # Flexibelt kort för dropdownen
                )
        ],width=6  # 3 delar av en 12-kolumn layout för tabellen och dropdown
        )
    ]), # Raden stängs här

        dbc.Row([
        dbc.Col([
            html.Hr(),
            html.H1("ALLA NATIONER", style={"textAlign": "center", "color": "black"}),
            html.Hr(),
        ])
    ],className="mb-3")
]) # App.layout stängs här


@callback(
    Output("dd_graph", "figure"),
    Input("dropdown-item", "value")
)

def update_graph(medal):
    if medal == "Gold":
        fig = px.line(df_pivot_g, title="Medaljer per År", labels={'value': 'Antal Medaljer'})
    elif medal == "Silver":
        fig = px.line(df_pivot_s, title="Medaljer per År", labels={'value': 'Antal Medaljer'})
    elif medal == "Bronze":
        fig = px.line(df_pivot_b, title="Medaljer per År", labels={'value': 'Antal Medaljer'})
    return fig


@callback(
    Output("dd_gender_graph", "figure"),
    Input("dropdown-gender-output", "value")
)

def update_graph(gender):
    pass

if __name__ == '__main__':
    app.run(debug=True)