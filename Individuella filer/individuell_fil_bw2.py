import pandas as pd   
import plotly.express as px
import dash            
from dash import dcc, html, Input, Output, Dash
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../athlete_events.csv")

app = Dash()

app.layout = [
    dcc.Dropdown(options=["Sailing", "Football", "Cross Country Skiing", "Handball"], value="Football", id='dropdown-item'),
    dcc.Graph(figure={}, id='controls-and-graph')
]

@app.callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='dropdown-item', component_property='value')
)
def update_graph(sport):
    dff=df[df["Sport"]==sport]
    fig = px.histogram(dff, x="Age", nbins=45, color="Sport", width=600)
    plt.show()
    return fig

if __name__ == '__main__':
    app.run(debug=True)


'''
Jennys grejs
'''


# plt.figure(figsize=(12,12))
# plt.subplot(3, 2, 1)
# df_sporter = df_anonym[df_anonym["Sport"].isin(["Cross Country Skiing"])]
# sns.set_theme(style="darkgrid")
# sns.histplot(x="Age", hue="Sport", data=df_sporter, binwidth=1, kde=True, palette=["Orange"])

# plt.title("Åldersfördelning i Längdskidor i OS")
# plt.xlabel("Ålder")
# plt.ylabel("Antal deltagare")

# plt.subplot(3, 2, 2)
# df_sporter = df_anonym[df_anonym["Sport"].isin(["Football"])]
# sns.set_theme(style="darkgrid")
# sns.histplot(x="Age", hue="Sport", data=df_sporter, binwidth=1, kde=True)

# plt.title("Åldersfördelning i Fotboll i OS")
# plt.xlabel("Ålder")
# plt.ylabel("Antal deltagare")

# plt.subplot(3, 2, 3)
# df_sporter = df_anonym[df_anonym["Sport"].isin(["Sailing"])]
# sns.set_theme(style="darkgrid")
# sns.histplot(x="Age", hue="Sport", data=df_sporter, binwidth=1, kde=True, palette=["Green"])

# plt.title("Åldersfördelning i Segling i OS")
# plt.xlabel("Ålder")
# plt.ylabel("Antal deltagare i procent")

# plt.subplot(3, 2, 4)
# df_sporter = df_anonym[df_anonym["Sport"].isin(["Handball"])]
# sns.set_theme(style="darkgrid")
# sns.histplot(x="Age", hue="Sport", data=df_sporter, binwidth=1, kde=True, palette=["Red"])

# plt.title("Åldersfördelning i Handboll i OS")
# plt.xlabel("Ålder")
# plt.ylabel("Antal deltagare")

# plt.tight_layout()
# plt.show()