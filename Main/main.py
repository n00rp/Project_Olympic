from dash import Dash, html, dash_table, dcc, Output, Input, callback
import pandas as pd
import plotly.express as px

df = pd.read_csv("../athlete_events.csv")

wo=["1948 Winter", "1952 Winter", "1956 Winter", "1960 Winter",
    "1964 Winter", "1968 Winter", "1972 Winter", "1976 Winter",
    "1980 Winter", "1984 Winter", "1988 Winter", "1992 Winter",
    "1994 Winter", "1998 Winter", "2002 Winter", "2006 Winter",
    "2010 Winter", "2014 Winter"]

# skapa df med endast längdskid-medaljörer
cc_delt=[]
for j in wo:
    df_year=df[df["Games"]==j]
    df_year_skidor=df_year[df_year["Sport"]=="Cross Country Skiing"]
    df_year_skidor_medals=df_year_skidor[df_year_skidor["Medal"].isin(["Gold", "Silver", "Bronze"])]
    medal_land=(len(df_year_skidor_medals["NOC"].unique()))
    delt_land=(len(df_year_skidor["NOC"].unique()))
    cc_delt.append([j, delt_land, medal_land])

df_cc_delt=pd.DataFrame(cc_delt, columns=["Games",  "Deltagarländer", "Medaljländer"])

app = Dash()

app.layout = [
    html.Div(children="Utveckling av längdskidor"),
    dcc.RadioItems(options=["Deltagarländer", "Medaljländer"], value="Deltagarländer", id='controls-and-radio-item'),
    dcc.Graph(figure={}, id='controls-and-graph')
]

@app.callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.line(df_cc_delt, x="Games", y=col_chosen)
    return fig

if __name__ == '__main__':
    app.run(debug=True)