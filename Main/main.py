import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import seaborn as sns

# Läs in data
df = pd.read_csv("Project_Olympic/athlete_events.csv")

# Definiera lista med vinter-OS
wo=["1948 Winter", "1952 Winter", "1956 Winter", "1960 Winter",
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
    df_sporter = df[df["Sport"].isin(["Curling", "Football", "Sailing", "Handball"])]
    sns.set_theme(style="darkgrid")
    fig, ax = plt.subplots()
    sns.histplot(x="Age", hue="Sport", data=df_sporter, bins=20, kde=True, ax=ax)
    return fig


# Skapa Dash-app
app = dash.Dash()

# Definiera app-layout
app.layout = [
    html.Div(children="Utveckling av längdskidor"),
    dcc.RadioItems(options=["Deltagarländer", "Medaljländer"], value="Deltagarländer", id='controls-and-radio-item'),
    dcc.Graph(figure={}, id='controls-and-graph'),
    html.Button('Visa länders prestation över tid', id='lander-prestation-button', n_clicks=0),
    dcc.Graph(id='lander-prestation-graph'),
    html.Button('Visa åldersfördelning', id='ålders-fördelning-button', n_clicks=0),
    dcc.Graph(id='ålders-fördelning'),
]

# Definiera callback-funktion för att uppdatera grafen
@app.callback(
    Output('controls-and-graph', 'figure'),
    [Input('controls-and-radio-item', 'value')]
)
def update_graph(col_chosen):
    fig = px.line(df_cc_delt, x="Games", y=col_chosen)
    return fig

# Definiera callback-funktion för att visa länders prestation över tid
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