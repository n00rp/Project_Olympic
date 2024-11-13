
import pandas as pd     
import plotly.express as px
import dash             
from dash import dcc, html, Input, Output

app = dash.Dash(__name__)

df=pd.read_csv("../athlete_events.csv")

app.layout = html.Div([

    html.Div([html.Label(['Välj en kategori'],style={'font-weight': 'bold', "text-align": "center"}),

        dcc.Dropdown(id='dropdown_meny',
            options=[
                     {'label': 'Land', 'value': 'NOC'},
                     {'label': 'Medalj', 'value': 'Medal'},
                     {'label': 'Sport', 'value': 'Sport'},
                     {'label': 'Kön', 'value': 'Sex'},
                     {'label': 'Stad', 'value': 'City'}
            ],
            optionHeight=25,                                      
            disabled=False,                     
            multi=False,                                                           
            placeholder='Välj...',     
            clearable=True,                     
            style={'width':"40%"},             
            ),  
        html.Div(id='output_data'),

        html.Div([
        dcc.Graph(id='olympic')
    ],className=""),

                                                             
                                                
    ],className=""),

])


@app.callback(
    Output(component_id='olympic', component_property='figure'),
    [Input(component_id='dropdown_meny', component_property='value')]
)

def build_graph(column_chosen):
    dff=df
    fig = px.pie(dff, names=column_chosen)
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title={'text':'Olympiska spel',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
