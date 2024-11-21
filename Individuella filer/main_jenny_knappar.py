import dash
from dash import Dash, html, dash_table, dcc, Output, Input, callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import seaborn as sns
import dash_bootstrap_components as dbc

# Läs in data
df = pd.read_csv("../athlete_events.csv")

# Definiera lista med vinter-OS
wo=["1924 Winter", "1928 Winter", "1932 Winter", "1936 Winter",
    "1948 Winter", "1952 Winter", "1956 Winter", "1960 Winter",
    "1964 Winter", "1968 Winter", "1972 Winter", "1976 Winter",
    "1980 Winter", "1984 Winter", "1988 Winter", "1992 Winter",
    "1994 Winter", "1998 Winter", "2002 Winter", "2006 Winter",
    "2010 Winter", "2014 Winter"]

# Skapa dataframes som används ofta
df_ger=df[df["NOC"]=="GER"]                                                 # Alla tyska deltagare
df_ger_medals=df_ger[df_ger["Medal"].isin(["Gold", "Silver", "Bronze"])]    # Alla tyska medaljörer

# Grafer utan callbacks

# Länder prestation över tid
lander_prestation_over_tid = df[(df['NOC'].isin(['GER', 'ITA', 'TUR', 'CHN', 'USA', 'FIN'])) & (df['Season'] == "Summer")].groupby(["NOC", "Year"])["Medal"].count().unstack().fillna(0)
fig2 = go.Figure()
for noc in lander_prestation_over_tid.index:
    noc_data = lander_prestation_over_tid.loc[noc]
    fig2.add_trace(go.Scatter(x=noc_data.index, y=noc_data.values, name=noc))
fig2.update_layout(title="Länders prestation över tid (Sommar-OS)", xaxis_title="År", yaxis_title="Medaljer")

# Länder som tagit medalj i längdskidor
df_skidor=df[df["Sport"]=="Cross Country Skiing"]
df_skidor_medaljer=df_skidor[df_skidor["Medal"].isin(["Gold", "Silver", "Bronze"])]
df_skidor_medaljer["NOC"].value_counts()

fig3=px.bar(df_skidor_medaljer["NOC"].value_counts(), labels={"NOC": "Land", "value": "Antal medaljer"}, title=("Länder som tagit medalj i längdskidor"))
fig3.update_layout(showlegend=False)

# Åldersfördelning
def ålders_fördelning_func():
    df_sporter = df[df["Sport"].isin(["Cross Country Skiing", "Football", "Sailing", "Handball"])]
    fig = px.histogram(df_sporter, x="Age", color="Sport", nbins=40, opacity=.4)
    return fig

# Skapa Dash-app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Definiera app-layout
app.layout = html.Div([
    html.Div([
        html.Div([
            dbc.Button("Visa graf", id="controls-and-graph-button", color="primary"),
            dbc.Collapse(
                dcc.Graph(figure=fig2, id='lander_prestation_over_tid-graph'),
                id="lander_prestation_over_tid-collapse",
            ),
        ], style={"padding": 10, "flex": 1, }),
        html.Div([
            dbc.Button("Visa graf", id="lander_skidor_medaljer-button", color="primary"),
            dbc.Collapse(
                dcc.Graph(figure=fig3, id='lander_skidor_medaljer-graph'),
                id="lander_skidor_medaljer-collapse",
            ),
        ], style={"padding": 10, "flex": 1, }),
    ], style={"display": "flex", "flexDirection": "row"}),
    
    html.Div([
        html.Div([
            dbc.Button("Visa graf", id="skidor_medaljer-button", color="primary"),
            dbc.Collapse(
                dcc.Graph(figure=fig3, id='skidor_medaljer-graph'),
                id="skidor_medaljer-collapse",
            ),
        ], style={"padding": 10, "flex": 1, }),
    ], style={"padding": 1, "flex": 1, }),
    html.Div([
        dcc.RadioItems(options=["M", "F"], value="M", id='langdvikt-radio'),
        dbc.Button("Visa graf", id="langdvikt-graph-button", color="primary"),
        dbc.Collapse(
            dcc.Graph(figure=ålders_fördelning_func(), id="langdvikt-graph-collapse")
        )
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
                          