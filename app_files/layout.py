import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, State, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import hashlib as hl
import random

app = Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])

app.layout = html.Div([

    dcc.Store(id='theme-store', data='light'),  # Lagrar det aktuella tema-värdet
    dcc.Dropdown(
        id='theme-dropdown',
        options=[
            {'label': 'Ljus', 'value': 'light'},
            {'label': 'Mörk', 'value': 'dark'}
        ],
        value='light'  # Standardvärde
    ),
    dbc.Card(
        dbc.CardBody([
            html.H2("Välkommen till Olympiska Spelen!", className="card-title"),
            html.P("Utforska medaljdata för Tyskland och andra nationer i de Olympiska spelen.", className="card-text, mb-4"),
            html.Img(src='/assets/os_ringar.png', className="mb-4", style={'width': '30%', 'display': 'block', 'margin': '0 auto'}),
        ]),
        className="mb-4 border-primary",  # Border och marginal
        style={"margin-top": "20px", "textAlign": "center"}
    ),

    # Rubrik för nästa sektion
    dbc.Card(
        dbc.CardBody([
            html.H1("TYSKLAND", style={"textAlign": "center", "color": "white", "fontSize": "3em"}),
        ]),
        className="mb-4 border-primary",  # Border och marginal
        style={"margin-top": "20px", "textAlign": "center"}
    ),

    # Flexbox container för vänster och höger card
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H4("Tyska Medaljer", className="card-title"),
                    dcc.Tabs([
                        dcc.Tab(label="Individuella medaljer", children=[medalj_individ()], style={'padding': '20px',"color": "black"}),
                        dcc.Tab(label="Nationella medaljer", children=[medalj_nation()], style={'padding': '20px', "color": "black"})
                    ])
                ]),
                className="mb-3", style={"max-width": "100%", "margin": "0 auto"}
            ),
            width=4  # 4 delar av en 12-kolumn layout för stort card
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
            width=2  # 2 delar av en 12-kolumn layout för den högerkolumnen med små cards
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
                        style_header={'fontWeight': 'bold'},
                        style_cell={'textAlign': 'center', 'padding': '10px', "color": "black"},                      
                    )
                ],className="table-striped table-bordered"), # Försöker lägga till temafärgen i tabellen
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

    ],className="mb-4"),# Raden stängs här
    
    dbc.Card(
        dbc.CardBody([
        html.Div([ 
        html.Div([
            dcc.RadioItems(options=["Deltagare", "Medaljer"], value="Deltagare", id='pie-radio', style={"fontSize": "20px"}),
            dcc.Graph(figure={}, id='pie-graph'),],style={"padding": 10, "flex":1, }),  
        html.Div([
            dcc.RadioItems(options=["Best", "Worst"], value="Best", id='bar-radio', style={"fontSize": "20px"}),
            dcc.Graph(figure={}, id='bar-graph'),],style={"padding": 10, "flex":1, }),                 
            ], style={"display": "flex", "flexDirection":"row"}),
        ])
    ),

    dbc.Card(
        dbc.CardBody([
            html.H1("ALLA NATIONER", style={"textAlign": "center", "color": "white"}),
        ]),
        className="mb-4 border-primary",  # Border och marginal
        style={"margin-top": "20px", "textAlign": "center"}
    ),

    dbc.Container([
         dbc.Card(
             dbc.CardBody([
                 dbc.Row([
                     dbc.Col([
                        dcc.Tabs(id='tabs', value='tab-2', children=[
                        dcc.Tab(label='Sommar OS', value='tab-2', style={"color": "black"}), # Bytte färg på text pga av tema, den vita texten försvann
                        dcc.Tab(label='Vinter OS', value='tab-3', style={"color": "black"}),
            ])], width=3),  # vänster kolumn

        dbc.Col([
            html.Div(id='tabs-content', children=[
                html.Div(id='tab-2-content', children=[
                    dcc.Dropdown(id='country-dropdown-2',
                                 options=[x for x in df['NOC'].unique()],
                                 multi=True,
                                 value=['USA', 'SWE'],
                                 style={'color': 'purple'}),                              
                    dcc.Dropdown(id='sport-dropdown',
                                 options=[{'label': sport, 'value': sport} for sport in sports],
                                 multi=True,
                                 value=['Athletics', 'Swimming'],
                                 style={'color': 'black'}),
                    dcc.Graph(id='figure2'),
                    dcc.Graph(id='figure-medals')
                ]),
                html.Div(id='tab-3-content', children=[
                    dcc.Dropdown(id='country-dropdown-3',
                                 options=[x for x in df['NOC'].unique()],
                                 multi=True,
                                 value=['USA', 'SWE'],
                                 style={'color': 'black'}),
                    dcc.Dropdown(id='sport-dropdown-3',
                                 options=[{'label': sport, 'value': sport} for sport in sports],
                                 multi=True,
                                 value=['Alpine Skiing', 'Figure Skating'],
                                 style={'color': 'black'}),
                    dcc.Graph(id='figure3'),
                    dcc.Graph(id='figure-medals-3')
                ])
            ])
        ], width=12)  # höger kolumn
    ])
             ]),className="mb-3"
         )
     ], fluid=True),

     dbc.Row([
         dbc.Col([
             dbc.Card(
                 dbc.CardBody([
                     dcc.Graph(figure=fig3)
                 ],style={"padding": 1, "flex":1, })
             )
         ]),
         dbc.Col([
             dbc.Card(
                 dbc.CardBody([
                     dcc.RadioItems(options=[
                            {"label": "Man", "value": "M"},
                            {"label": "Kvinna", "value": "F"}], value="M", id='langdvikt-radio', style={"fontSize": "20px"}), # Ökat storleken på radioitem text
                     dcc.Graph(figure={}, id="langdvikt-graph")
                 ],style={"padding": 1, "flex":1, })
             )
         ]),
         dbc.Col([
             dbc.Card(
                 dbc.CardBody([
                    dcc.RadioItems(options=["Winter games", "Summer games"], value="Winter games", id='coldwar-radio', style={"fontSize": "20px"}),
                    dcc.Graph(figure={}, id="coldwar-graph")
                 ],style={"padding": 1, "flex":1, })
             )
         ])
     ], className="mb-5"),

     dbc.Row([
         dbc.Col([
             dbc.Card(
                 dbc.CardBody([
                     dcc.RadioItems(options=["Deltagarländer", "Medaljländer"], value="Deltagarländer", id='controls-and-radio-item', style={"fontSize": "20px"}),
                     dcc.Graph(figure={}, id='controls-and-graph')
                 ],style={"padding": 10, "flex":1, })
             )
         ],width=5),
         dbc.Col([
             dbc.Card(
                 dbc.CardBody([
                     dcc.Markdown("Åldersfördelning i respektive sport"),
                     dcc.Dropdown(id='sport',
                         options=[x for x in ["Sailing", "Curling", "Football", "Handball"]],
                         multi=True,
                         value=['Curling', 'Handball']),
                         dcc.Graph(id='figure1')   
                 ])
             )
         ])
     ], className="mb-5"),

        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                            html.H1("Åldersfördelning i OS"),
                            dcc.Dropdown(
                                id="sport-dropdown1",
                                options=[{"label": sport, "value": sport} for sport in sports],
                                value=sports[0]),
                            dcc.Graph(id="age-graph")
                    ])
                )
            ])
        ])

])