import dash
from dash import Dash, html, dash_table, dcc, Output, Input, callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import seaborn as sns

# Läs in data
df = pd.read_csv("../athlete_events.csv")

# Definiera lista med vinter-OS
wo=["1924 Winter", "1928 Winter", "1932 Winter", "1936 Winter",
    "1948 Winter", "1952 Winter", "1956 Winter", "1960 Winter",
    "1964 Winter", "1968 Winter", "1972 Winter", "1976 Winter",
    "1980 Winter", "1984 Winter", "1988 Winter", "1992 Winter",
    "1994 Winter", "1998 Winter", "2002 Winter", "2006 Winter",
    "2010 Winter", "2014 Winter"]

# Skapa df med endast längdskid-medaljörer
cc_delt=[]
for j in wo:
    df_year=df[df["Games"]==j]
    df_year_skidor=df_year[df_year["Sport"]=="Cross Country Skiing"]
    df_year_skidor_medals=df_year_skidor[df_year_skidor["Medal"].isin(["Gold", "Silver", "Bronze"])]
    medal_land=(len(df_year_skidor_medals["NOC"].unique()))
    delt_land=(len(df_year_skidor["NOC"].unique()))
    cc_delt.append([j, delt_land, medal_land])
df_cc_delt=pd.DataFrame(cc_delt, columns=["Games",  "Deltagarländer", "Medaljländer"])

# Skapa df med Tysklands 10-i-topp-sporter sett till deltagare respektive medaljer
df_ger=df[df["NOC"]=="GER"]
df_ger_medals=df_ger[df_ger["Medal"].isin(["Gold", "Silver", "Bronze"])]
top10_deltag=df_ger["Sport"].value_counts().head(10)
top10_medalj=df_ger_medals["Sport"].value_counts().head(10)
ger_deltagare=top10_deltag.to_frame(name="Deltagare")
ger_medaljer=top10_medalj.to_frame(name="Medaljer")
ger_delt_och_med=pd.concat([ger_deltagare, ger_medaljer], axis=1)

# skapa df med tysklands procentuellt bästa sporter (medaljer i förhållande till deltagare)
deltag=df_ger["Sport"].value_counts()       # antal tyska deltagare per sport
medalj=df_ger_medals["Sport"].value_counts()    # antal tyska medaljörer per sport

ger_deltagare=deltag.to_frame(name="Deltagare")     
ger_medaljer=medalj.to_frame(name="Medaljer")
ger_percent=pd.concat([ger_deltagare, ger_medaljer], axis=1)
ger_percent["Procent"]=100*ger_percent["Medaljer"]/ger_percent["Deltagare"]
ger_percent=ger_percent.sort_values("Procent", ascending=False)

ger_percent=ger_percent[(ger_percent["Deltagare"]>=20) & (ger_percent["Medaljer"]>=1)]
ger_percent1=ger_percent.head(19).rename(columns={"Procent": "Best"})
ger_percent2=ger_percent.tail(19).rename(columns={"Procent": "Worst"})

bestworst=pd.concat([ger_percent1, ger_percent2])
colors=["#cc3333"]


# Definiera funktion för att generera graf för länders prestation över tid
def länder_prestation_över_tid_graph():
    lander_prestation_over_tid = df[(df['NOC'].isin(['GER', 'ITA', 'TUR', 'CHN', 'USA', 'FIN'])) & (df['Season'] == "Summer")].groupby(["NOC", "Year"])["Medal"].count().unstack().fillna(0)
    fig = go.Figure()
    for noc in lander_prestation_over_tid.index:
        noc_data = lander_prestation_over_tid.loc[noc]
        fig.add_trace(go.Scatter(x=noc_data.index, y=noc_data.values, name=noc))
    fig.update_layout(title="Länders prestation över tid (Sommar-OS)", xaxis_title="År", yaxis_title="Medaljer")
    return fig

def ålders_fördelning_func():
    df_sporter = df[df["Sport"].isin(["Cross Country Skiing", "Football", "Sailing", "Handball"])]
    fig = px.histogram(df_sporter, x="Age", color="Sport", nbins=40, opacity=.4)
    return fig

def langd_och_vikt_func():
    df_ger=df[df["NOC"]=="GER"]
    df_vikt=df_ger[df_ger["Sport"].isin(["Gymnastics", "Handball", "Weightlifting", "Ski Jumping"])]
    fig = px.scatter(df_vikt, x="Height", range_x=[130,220], y="Weight", range_y=[20,140], animation_frame="Sex", color="Sport", opacity=.4)
    return fig



# Skapa Dash-app
app = dash.Dash()

# Definiera app-layout
app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.RadioItems(options=["Deltagarländer", "Medaljländer"], value="Deltagarländer", id='controls-and-radio-item'),
            dcc.Graph(figure={}, id='controls-and-graph'),],style={"padding": 10, "flex":1, }),
        html.Div([
            html.Button('Visa länders prestation över tid', id='lander-prestation-button', n_clicks=0),
            dcc.Graph(id='lander-prestation-graph'),],style={"padding": 10, "flex":1, }),
            ], style={"display": "flex", "flexDirection":"row"}),
        
    html.Div([    
        html.Div([
            html.Button('Visa åldersfördelning', id='ålders-fördelning-button', n_clicks=0),
            dcc.Graph(id='ålders-fördelning'),],style={"padding": 10, "flex":1, }),
        html.Div([
            html.Button('Visa längd och vikt', id='langd-vikt-button', n_clicks=0),
            dcc.Graph(id='langd-vikt-graph'),],style={"padding": 10, "flex":1, })
            ], style={"display": "flex", "flexDirection":"row"}),

    html.Div([ 
        html.Div([
            dcc.RadioItems(options=["Deltagare", "Medaljer"], value="Deltagare", id='pie-radio'),
            dcc.Graph(figure={}, id='pie-graph'),],style={"padding": 10, "flex":1, }),  
        html.Div([
            dcc.RadioItems(options=["Best", "Worst"], value="Best", id='bar-radio'),
            dcc.Graph(figure={}, id='bar-graph'),],style={"padding": 10, "flex":1, }),                 
            ], style={"display": "flex", "flexDirection":"row"}),
    
    ])



# Definiera callback-funktion för att uppdatera grafen
@app.callback(
    Output('controls-and-graph', 'figure'),
    [Input('controls-and-radio-item', 'value')]
)
def update_graph(col_chosen):
    fig = px.line(df_cc_delt, x="Games", y=col_chosen)
    return fig

# Pie chart med top 10-sporter
@app.callback(
    Output('pie-graph', 'figure'),
    [Input('pie-radio', 'value')]
)
def update_graph(val):
    fig = px.pie(ger_delt_och_med, values=val, names=ger_delt_och_med.index, title="Tysklands 10 största sporter")
    return fig

# Bar chart med procentuellt bästa/sämsta sporterna
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('bar-radio', 'value')]
)
def update_graph(barval):
    fig=px.histogram(bestworst, x=bestworst.index, y=barval, color_discrete_sequence=colors, title="Tysklands procentuellt bästa och sämsta grenar")
    fig.update_layout(yaxis_title="Procent")
    return fig


@app.callback(
    Output('langd-vikt-graph', 'figure'),
    [Input('langd-vikt-button', 'n_clicks')]
)

def langd_och_vikt(n_clicks):
    if n_clicks > 0:
        return langd_och_vikt_func()
    else:
        return {}

@app.callback(
    Output('lander-prestation-graph', 'figure'),
    [Input('lander-prestation-button', 'n_clicks')]
)

def update_lander_prestation_graph(n_clicks):
    if n_clicks > 0:
        return länder_prestation_över_tid_graph()
    else:
        return {}
    
@app.callback(
    Output("ålders-fördelning", "figure"),
    [Input("ålders-fördelning-button", "n_clicks")]
)
def ålders_fördelning(n_clicks):
    if n_clicks > 0:
        return ålders_fördelning_func()
    else:
        return {}
# Kör appen
if __name__ == '__main__':
    app.run(debug=True)