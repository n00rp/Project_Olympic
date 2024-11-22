import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, State, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import hashlib as hl
import random

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