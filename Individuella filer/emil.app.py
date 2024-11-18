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
fig = px.bar(medals, x="Medal", color="Medal", color_discrete_sequence=color1, width=500, height=500)
fig.update_layout(title="Tyska Induviduella Medaljer", xaxis_title="Valör", yaxis_title="Antal")


""" Tabell på medaljer som nation i Tyskland """
temp_df = ger_df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
ny_team_variabel = temp_df["Medal"].isin(["Gold", "Silver", "Bronze"])
ny_team_variabel = temp_df[ny_team_variabel]
fig = px.bar(ny_team_variabel, x="Medal", color="Medal", color_discrete_sequence=color1, width=500, height=500)
fig.update_layout(title="Tyska Nationella Medaljer", xaxis_title="Valör", yaxis_title="Antal")
#----------------------------------------------------------------------------------------------------------------

app = Dash()

app.layout = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            html.H3(children="Tyska Nationella Medaljer"),
            html.Img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Flag_of_Germany.svg/1200px-Flag_of_Germany.svg.png"),
            dcc.Graph(
                id="ger-team-medals",
                figure=fig
            )], style={"padding": 10, "flex":1, }),
        html.Div(children=[
            html.H3(children="Tyska Induviduella Medaljer"),
            html.Img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Flag_of_Germany.svg/1200px-Flag_of_Germany.svg.png"),
            dcc.Graph(
                id="ger-indv-medals",
                figure=fig
            )], style={"padding": 10, "flex":1, })
            ], style={"display": "flex", "flexDirection":"row"}),
   
    ])
    

if __name__ == '__main__':
    app.run(debug=True)