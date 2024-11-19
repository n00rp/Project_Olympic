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

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# app.layout = html.Div([
#     # Lägg till en bild
#     html.Img(src='/assets/os_ringar.png', style={'width': '30%', 'display': 'block', 'margin': '0 auto'}),

#     # Lägg till padding-top och bakgrundsfärg
#     html.Div(className="pt-5"),

#     # Rubrik för OLYMPISKA SPELEN
#     html.H1("OLYMPISKA SPELEN", style={"textAlign": "center", "color": "blue"}),

#     # Horisontell linje
#     html.Hr(),

#     # Lägg till padding-top och bakgrundsfärg
#     html.Div(className="pt-5"),

#     # Rubrik för nästa sektion
#     html.H1("TYSKLAND", style={"textAlign": "center", "color": "black"}),

#     # Card för att visa medaljgrafen
#     dbc.Card(
#         dbc.CardBody([
#             html.H4("Tyska Medaljer", className="card-title"),
#             # Tabs-komponenten som innehåller två flikar
#             dcc.Tabs([
#                 dcc.Tab(label="Nationella medaljer", children=[
#                     medalj_individ()  # Graf för den första fliken
#                 ], style={'padding': '10px'}),
                
#                 dcc.Tab(label="Induviduella medaljer", children=[
#                     medalj_nation()  # Graf för den andra fliken
#                 ], style={'padding': '10px'})
#             ])
#         ]),
#         className="border-primary mb-3",  # Bootstrap-klasser för att få en bård runt hela carden
#         style={"max-width": "30%", "margin": "0 auto"}  # Gör carden centrerad
#     )
# ])

app.layout = html.Div([
    # Lägg till en bild
    html.Img(src='/assets/os_ringar.png', style={'width': '30%', 'display': 'block', 'margin': '0 auto'}),

    # Lägg till padding-top och bakgrundsfärg
    html.Div(className="pt-5"),

    # Rubrik för OLYMPISKA SPELEN
    html.H1("OLYMPISKA SPELEN", style={"textAlign": "center", "color": "blue"}),

    # Horisontell linje
    html.Hr(),

    # Lägg till padding-top och bakgrundsfärg
    html.Div(className="pt-5"),

    # Rubrik för nästa sektion
    html.H1("TYSKLAND", style={"textAlign": "center", "color": "black"}),

    # Flexbox container
    html.Div(
        className="d-flex",  # Använd flexbox för att placera cards sida vid sida
        children=[
            # Card till vänster (30% bredd)
            html.Div(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Tyska Medaljer", className="card-title"),
                        dcc.Tabs([
                            dcc.Tab(label="Medaljer 1", children=[medalj_individ()], style={'padding': '20px'}),
                            dcc.Tab(label="Medaljer 2", children=[medalj_nation()], style={'padding': '20px'})
                        ])
                    ]),
                    className="border-primary mb-3", 
                    style={"max-width": "100%", "margin": "0 auto"}
                ),
                style={"width": "30%", "padding": "10px"}  # 30% bredd på vänster card
            ),
            
            # Card till höger (70% bredd)
            html.Div(
                dbc.Card(
                    dbc.CardBody([
                        # Flexbox container för små cards
                        html.Div(
                            className="d-flex flex-column",  # Flexbox och vertikal layout
                            children=[
                                # Första lilla cardet
                                dbc.Card(
                                    dbc.CardBody([
                                        html.Img(src='/assets/silver.png', style={'width': '7%'}),
                                        html.H4("745", className="card-text")
                                    ]),
                                    className="mb-3",  # Marginal mellan cards
                                    style={"height": "100%"}  # Gör alla cards lika höga
                                ),

                                # Andra lilla cardet
                                dbc.Card(
                                    dbc.CardBody([
                                        html.Img(src='/assets/silver.png', style={'width': '7%'}),
                                        html.H4("674", className="card-text")
                                    ]),
                                    className="mb-3",  # Marginal mellan cards
                                    style={"height": "100%"}
                                ),

                                # Tredje lilla cardet
                                dbc.Card(
                                    dbc.CardBody([
                                        html.Img(src='/assets/bronz.png', style={'width': '7%'}),
                                        html.H4("746", className="card-text")
                                    ]),
                                    className="mb-3",  # Marginal mellan cards
                                    style={"height": "100%"}
                                ),
                            ]
                        ),
                    ]),

                ),

            ),
        ]
    ),
])


if __name__ == '__main__':
    app.run(debug=True)