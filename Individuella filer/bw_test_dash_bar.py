
import pandas as pd 
import datetime as dt
import dash         
from dash import dcc, html, Input, Output

import plotly     
import plotly.express as px

df = pd.read_csv("../athlete_events.csv")

df = df[(df["Medal"].isin(["Gold", "Silver", "Bronze"]))]

app = dash.Dash(__name__)

app.layout = html.Div([


        html.Div([
            html.Label(['Kategorier att jämföra'],style={'font-weight': 'bold'}),
            dcc.RadioItems(
                id='xaxis_raditem',
                options=[
                         {'label': 'Medalj', 'value': 'Medal'},
                         {'label': 'Kön', 'value': 'Sex'},
                ],
                value="Sex",
                style={"width": "90%"}
            ),
        ]),

        html.Div([
            html.Br(),
            html.Label(['Y-värden att jämföra:'], style={'font-weight': 'bold'}),
            dcc.RadioItems(
                id='yaxis_raditem',
                options=[
                         {'label': 'Ålder', 'value': 'Age'},
                         {'label': 'Längd', 'value': 'Height'},
                ],
                value="Age",
                style={"width": "50%"}
            ),
        ]),

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

])

#-------------------------------------------------------------------------------------
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='xaxis_raditem', component_property='value'),
     Input(component_id='yaxis_raditem', component_property='value')]
)

def update_graph(x_axis, y_axis):

    dff = df
   
    barchart=px.histogram(
            data_frame=dff,
            x=x_axis,
            y=y_axis,
            histfunc="avg",
            color="Medal"
            )

    barchart.update_layout(xaxis={'categoryorder':'total ascending'},
                           title={'xanchor':'center', 'yanchor': 'top', 'y':0.9,'x':0.5,})

    return (barchart)

if __name__ == '__main__':
    app.run_server(debug=True)