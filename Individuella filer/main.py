import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, State, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import hashlib as hl
import random
#--------------------------------------------------------------------------------------------------------------
df = pd.read_csv("../athlete_events.csv")


""" hashar namnen och droppar namn kolumnen """
hashes = df["Name"].apply(lambda client_num: hl.sha256(client_num.encode()).hexdigest())
df.insert(1, "SHA Hash Values", hashes)
drop = df.drop(columns= ["Name"])
df = drop

""" Tar alla unika sporter """
sports = df['Sport'].unique()

""" Tabell på antal medaljer per individ i tyskland """
ger_df = df[df["NOC"] == "GER"]
medal = ger_df["Medal"].isin(["Gold", "Silver", "Bronze"])
medals = ger_df[medal]
color1 = ["silver", "orange", "gold"]

"""" Filtrering av medaljer """
df_ger=df[df["NOC"]=="GER"]                                                 # Alla tyska deltagare
df_ger_medals=df_ger[df_ger["Medal"].isin(["Gold", "Silver", "Bronze"])]  

""" Tabell på medaljer som nation i Tyskland """
temp_df = ger_df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
ny_team_variabel = temp_df["Medal"].isin(["Gold", "Silver", "Bronze"])
ny_team_variabel = temp_df[ny_team_variabel]
test = ny_team_variabel.copy()


""" Tabell på medaljer """
test.loc[:, "Medaltot"] = 1
df_grouped = test.groupby(['Year', 'Medal']).sum().reset_index()
df_pivot = df_grouped.pivot(index='Year', columns='Medal', values='Medaltot')# Pivot = Year blir x-axeln och Medal blir kolumner med en valör i varje. Values(Medeltot) får summan av varje valör per år.
df_pivot_g = df_pivot["Gold"]
df_pivot_s = df_pivot["Silver"]
df_pivot_b = df_pivot["Bronze"]

""" Filtrering av medaljer inom skidor """
# Länder som tagit medalj i längdskidor
df_skidor=df[df["Sport"]=="Cross Country Skiing"]
df_skidor_medaljer=df_skidor[df_skidor["Medal"].isin(["Gold", "Silver", "Bronze"])]
df_skidor_medaljer["NOC"].value_counts()

fig3=px.bar(df_skidor_medaljer["NOC"].value_counts(), labels={"NOC": "Land", "value": "Antal medaljer"}, title=("Länder som tagit medalj i längdskidor"))
fig3.update_layout(showlegend=False)

# Definiera lista med vinter-OS
wo=["1924 Winter", "1928 Winter", "1932 Winter", "1936 Winter",
    "1948 Winter", "1952 Winter", "1956 Winter", "1960 Winter",
    "1964 Winter", "1968 Winter", "1972 Winter", "1976 Winter",
    "1980 Winter", "1984 Winter", "1988 Winter", "1992 Winter",
    "1994 Winter", "1998 Winter", "2002 Winter", "2006 Winter",
    "2010 Winter", "2014 Winter"]

# Räknar antalet män och kvinnor över tid i OS.
df_os_kon = df.groupby(["Year", "Season", "Sex"])["Name"].count().reset_index()
df_os_kon = df_os_kon.rename(columns={"Name": "Antal"})
sommar_os = df_os_kon[df_os_kon["Season"] == "Summer"]
vinter_os = df_os_kon[df_os_kon["Season"] == "Winter"]

#----------------------------------------------------------------------------------------------------------------


def medalj_individ():
    fig = px.bar(medals, x="Medal", color="Medal", color_discrete_sequence=color1, width=590, height=650)
    fig.update_layout(title="Tyska Individuella Medaljer", xaxis_title="Valör", yaxis_title="Antal")
    fig.update_xaxes(categoryorder="array", categoryarray=["Gold", "Silver", "Bronze"])
    return dcc.Graph(id="medalj_individ", figure=fig)

def medalj_nation():
    fig = px.bar(ny_team_variabel, x="Medal", color="Medal", color_discrete_sequence=color1, width=590, height=650)
    fig.update_layout(title="Tyska Nationella Medaljer", xaxis_title="Valör", yaxis_title="Antal")
    fig.update_xaxes(categoryorder="array", categoryarray=["Gold", "Silver", "Bronze"])
    return dcc.Graph(id="medalj_nation", figure=fig)

#------------------------------------------------------------------------------------------------------------------

app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])
server = app.server
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
                        dcc.Tab(label='Sommar-OS', value='tab-2', style={"color": "black"}), # Bytte färg på text pga av tema, den vita texten försvann
                        dcc.Tab(label='Vinter-OS', value='tab-3', style={"color": "black"}),
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
                            {"label": " Man", "value": "M"},
                            {"label": " Kvinna", "value": "F"}], value="M", id='langdvikt-radio', style={"fontSize": "20px"}), # Ökat storleken på radioitem text
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
                     dcc.RadioItems(options=[" Deltagarländer", " Medaljländer"], value="Deltagarländer", id='controls-and-radio-item', style={"fontSize": "20px"}),
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
            ],width=5),
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                            html.H1("Könsfördelningen i Sommar OS över tid"),
                            dcc.RadioItems(options=["Summer games", "Winter games"], value="Winter games", id='gender-radio', style={"fontSize": "20px"}),
                            dcc.Graph(id="gender-graph")
                    ],style={"padding": 7, "flex":1, })
                )
            ])
        ])

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
    fig.update_layout(legend_title="Medalj")
    return fig

@callback(
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

@callback(
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


@callback(
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
@callback(
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

@callback(
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

@app.callback(
    Output('pie-graph', 'figure'),
    [Input('pie-radio', 'value')]
)
def top_tio_graf(val):
    top10_deltag=df_ger["Sport"].value_counts().head(10)
    top10_medalj=df_ger_medals["Sport"].value_counts().head(10)
    ger_deltagare=top10_deltag.to_frame(name="Deltagare")
    ger_medaljer=top10_medalj.to_frame(name="Medaljer")
    ger_delt_och_med=pd.concat([ger_deltagare, ger_medaljer], axis=1)
    fig = px.pie(ger_delt_och_med, values=val, names=ger_delt_och_med.index, title="Tysklands 10 största sporter")
    return fig

# Bar chart med procentuellt bästa/sämsta sporterna
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('bar-radio', 'value')]
)
def update_graph(barval):
    deltag=df_ger["Sport"].value_counts()       # antal tyska deltagare per sport
    medalj=df_ger_medals["Sport"].value_counts()    # antal tyska medaljörer per sport
    ger_deltagare=deltag.to_frame(name="Deltagare")     
    ger_medaljer=medalj.to_frame(name="Medaljer")
    ger_percent=pd.concat([ger_deltagare, ger_medaljer], axis=1)
    ger_percent=ger_percent[(ger_percent["Deltagare"]>=20) & (ger_percent["Medaljer"]>=1)]  # Rensa bort sporter som är för små
    ger_percent["Procent"]=100*ger_percent["Medaljer"]/ger_percent["Deltagare"]
    ger_percent=ger_percent.sort_values("Procent", ascending=False)

    ger_percent1=ger_percent.head(18).rename(columns={"Procent": "Best"})
    ger_percent2=ger_percent.tail(18).rename(columns={"Procent": "Worst"})

    bestworst=pd.concat([ger_percent1, ger_percent2])
    colors=["#cc3333"]
    fig=px.histogram(bestworst, x=bestworst.index, y=barval, color_discrete_sequence=colors, title="Tysklands procentuellt bästa och sämsta grenar")
    fig.update_layout(yaxis_title="Procent")
    return fig

@callback(
    Output('langdvikt-graph', 'figure'),
    [Input('langdvikt-radio', 'value')]
)

def langd_och_vikt_func(gender_choice):
    df_vikt=df_ger[df_ger["Sport"].isin(["Gymnastics", "Handball", "Weightlifting", "Ski Jumping"])]
    df_gender=df_vikt[df_vikt["Sex"]==gender_choice]
    fig = px.scatter(df_gender, x="Height", range_x=[130,220], y="Weight", range_y=[20,140], color="Sport", opacity=.4)
    return fig

@app.callback(
    Output('coldwar-graph', 'figure'),
    [Input('coldwar-radio', 'value')]
)

def coldwar_func(sw_choice):
    df_frg_gdr=df[df["NOC"].isin(["FRG", "GDR"])]
    games_cold_war_s=["1968 Summer", "1972 Summer", "1976 Summer", "1980 Summer", "1984 Summer", "1988 Summer"]
    games_cold_war_w=["1968 Winter", "1972 Winter", "1976 Winter", "1980 Winter", "1984 Winter", "1988 Winter"]
    df_frg_gdr=df_frg_gdr[df_frg_gdr["Year"].isin([1968, 1972, 1976, 1980, 1984, 1988])]
    df_frg_gdr=df_frg_gdr[df_frg_gdr["Medal"].isin(["Gold", "Silver", "Bronze"])]
    df_frg_gdr["Medaltot"]=1
    df_frg_gdr["Winter games"]=None
    df_frg_gdr["Summer games"]=None
    mask1=df_frg_gdr["Games"].isin(games_cold_war_w)
    mask2=df_frg_gdr["Games"].isin(games_cold_war_s)
    df_frg_gdr.loc[mask1, "Winter games"]=df_frg_gdr.loc[mask1, "Games"]
    df_frg_gdr.loc[mask2, "Summer games"]=df_frg_gdr.loc[mask2, "Games"]
    df_frg_gdr=df_frg_gdr.sort_values(by=["Year"])

    fig=px.histogram(df_frg_gdr, x=sw_choice, y="Medaltot", color="NOC", barmode="group")
    fig.update_xaxes(categoryorder="array", categoryarray=games_cold_war_s)
    fig.update_yaxes(title="Antal medaljer")
    return fig

# Deltagarländer och medaljländer i längdskidåkning
@app.callback(
    Output('controls-and-graph', 'figure'),
    [Input('controls-and-radio-item', 'value')]
)
def cross_country_countries(cc_yval):
    cc_delt=[]
    for j in wo:
        df_year=df[df["Games"]==j]
        df_year_skidor=df_year[df_year["Sport"]=="Cross Country Skiing"]
        df_year_skidor_medals=df_year_skidor[df_year_skidor["Medal"].isin(["Gold", "Silver", "Bronze"])]
        medal_land=(len(df_year_skidor_medals["NOC"].unique()))
        delt_land=(len(df_year_skidor["NOC"].unique()))
        cc_delt.append([j, delt_land, medal_land])
    cross_country_lander=pd.DataFrame(cc_delt, columns=["Games",  "Deltagarländer", "Medaljländer"])
    fig = px.line(cross_country_lander, x="Games", y=cc_yval)
    fig.update_xaxes(title_font_size=7)
    return fig   

@app.callback(
    Output('figure1','figure'),
    Input('sport', 'value')
)
def age_histogram(sport_selected):
    df_filtered = df[df.Sport.isin(sport_selected)]
    fig = px.histogram(df_filtered, x='Age', color='Sport', opacity=.4, range_x=[10,70], range_y=[0,1000], barmode="overlay")

    return fig

# Definiera en funktion som uppdaterar grafen när användaren väljer en ny sport
@app.callback(
    Output("age-graph", "figure"),
    [Input("sport-dropdown1", "value")]
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

@app.callback(
    Output("gender-graph", "figure"),
    [Input("dropdown-gender-output", "value")])

def update_graph(gender):
    


if __name__ == '__main__':
    app.run(debug=True)


