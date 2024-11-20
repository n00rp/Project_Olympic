import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd

from dash import Dash, html, dcc, callback, Output, Input, State, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
#--------------------------------------------------------------------------------------------------------------
df = pd.read_csv("athlete_events.csv")

# """ Tabell på antal medaljer per individ i tyskland """
# ger_df = df[df["NOC"] == "GER"]
# ger_df1 = pd.concat([ger_df,pd.get_dummies(df["Medal"])],axis = 1)
# ger_indv_medals = ger_df1.groupby("NOC").sum()[["Gold","Silver","Bronze"]].sort_values("Gold",ascending=False).reset_index()

# """ Tabell på medaljer som nation i Tyskland """
# # Filtrering på alla dubletter som förekommer av valda kolumner
# temp_df = df.dropna(subset=["Medal"])
# temp_df = df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
# # Droppar alla nan i medaljkolumnen, listar alla länder
# cleaned_df =temp_df.dropna(subset=["Medal"])
# ger_df_team = cleaned_df[cleaned_df["NOC"] == "GER"]
# cleaned_df1 = pd.concat([ger_df_team, pd.get_dummies(ger_df_team["Medal"], prefix='Medal')], axis=1)
# cleaned_df1
# ger_team_medals = cleaned_df1.groupby("NOC").sum()[["Medal_Gold", "Medal_Silver", "Medal_Bronze"]].sort_values("Medal_Gold", ascending=False).reset_index()

""" Tabell på antal medaljer per individ i tyskland """
ger_df = df[df["NOC"] == "GER"]
medal = ger_df["Medal"].isin(["Gold", "Silver", "Bronze"])
medals = ger_df[medal]
color1 = ["silver", "orange", "gold"]

""" Tabell på medaljer som nation i Tyskland """
temp_df = ger_df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
ny_team_variabel = temp_df["Medal"].isin(["Gold", "Silver", "Bronze"])
ny_team_variabel = temp_df[ny_team_variabel]
fig = px.bar(ny_team_variabel, x="Medal", color="Medal", color_discrete_sequence=color1, width=500, height=500)
fig.update_layout(title="Tyska Nationella Medaljer", xaxis_title="Valör", yaxis_title="Antal")
#----------------------------------------------------------------------------------------------------------------

def medalj_individ():
    fig = px.bar(medals, x="Medal", color="Medal", color_discrete_sequence=color1, width=500, height=500)
    fig.update_layout(title="Tyska Individuella Medaljer", xaxis_title="Valör", yaxis_title="Antal")
    return dcc.Graph(id="medalj_individ", figure=fig)

def medalj_nation():
    fig = px.bar(ny_team_variabel, x="Medal", color="Medal", color_discrete_sequence=color1, width=500, height=500)
    fig.update_layout(title="Tyska Nationella Medaljer", xaxis_title="Valör", yaxis_title="Antal")
    return dcc.Graph(id="medalj_nation", figure=fig)

#------------------------------------------------------------------------------------------------------------------

# dash_table.DataTable(
#     cities = [
#             {"name": "Stad", "id": "stad"},
#             {"name": "Typ av OS", "id": "os_type"},
#             {"name": "År", "id": "year"}
#         ],
#     data=[
#             {"stad": "Berlin", "os_type": "Sommar OS", "year": "1916 (Inställt)"}
#             {"stad": "Berlin", "os_type": "Sommar OS", "year": "1936"}
#             {"stad": "Garmisch-Partenkirchen", "os_type": "Vinter OS", "year": "1936"}
#         ],
#         style_table={'width': '50%', 'margin': '0 auto'},  # Centrera tabellen på sidan och sätt bredd
#         style_header={'backgroundColor': 'lightblue', 'fontWeight': 'bold'},  # Rubriker
#         style_cell={'textAlign': 'center', 'padding': '10px'},  # Cellstil
#         )

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([

    # Övergripande Card högst upp på sidan
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
                className="border-primary mb-3", style={"max-width": "100%", "margin": "0 auto"}
            ),
            width=5  # 8 delar av en 12-kolumn layout för stort card
        ),

        # Liten Col för de tre små cardsen (4/12 bredd)
        dbc.Col(
            # Här placeras de tre små cardsen vertikalt i samma kolumn
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
        ),

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

                        )
                    ]),
                    className="mb-3", style={"height": "auto", "width": "150%"}  # Flexibelt kort för tabellen
                ),
            dbc.Card(
            dbc.CardBody([
            dcc.Graph(figure={}, id="line-fig", style={"height": "400px", "width": "100%"})
            ]),
            className="mb-3", style={"width": "150%"}  # Flexibelt kort för grafen
        )
            ],
            width=3  # 3 delar av en 12-kolumn layout för tabellen och grafen
        ) 
    ])

])


if __name__ == '__main__':
    app.run(debug=True)