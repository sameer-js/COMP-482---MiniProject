import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


poison = pd.read_csv(
    'nchs-drug-poisoning-mortality-united-states.csv')

poison = poison[poison['Age'] != 'All Ages']

poison.fillna(0, inplace=True)

poison.drop(["Low Confidence Limit for Crude Rate",
            "Upper Confidence Limit for Crude Rate", "Age-adjusted Rate", "US Crude Rate"], axis=1).head()

app = dash.Dash(__name__, meta_tags=[
                {"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div((

    html.Div([
        html.Div([
            html.Div([
                html.H3('Data Analysis on Drug Poisoning Mortality (US)', style={
                        'margin-top': '-30px', 'color': 'black'}),
            ])
        ], className="create_container1 four columns", id="title"),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

    html.Div([

        html.Div([
             html.Div(id='text1'),

             ], className="create_container2 three columns"),

        html.Div([
            dcc.Graph(id='line_chart',
                      config={'displayModeBar': None}),
        ], className="create_container2 five columns", style={'height': '150px'}),

        html.Div([
            html.Div(id='text2'),

        ], className="create_container2 two columns"),


        html.Div([
            html.Div(id='text3'),

        ], className="create_container2 two columns"),

    ], className="row flex-display"),


    html.Div([
        html.Div([

            html.P('Select Year', className='fix_label', style={'color': '#3065C9',
                                                                'margin-top': '30px',
                                                                'margin-bottom': '30px',
                                                                'text-align': 'center'}),
            dcc.Slider(id='select_year',
                       included=False,
                       updatemode='drag',
                       tooltip={'always_visible': True},
                       min=1999,
                       max=2015,
                       step=1,
                       value=2006,
                       marks={str(yr): str(yr) for yr in range(1999, 2015, 5)},
                       className='dcc_compon'),

            html.P('Select Origin', className='fix_label',  style={
                   'color': '#3065C9', 'text-align': 'center'}),
            dcc.Dropdown(id='select_origin',
                         multi=False,
                         clearable=True,
                         disabled=False,
                         style={'display': True},
                         value='Other Orign',
                         placeholder='Select Origin',
                         options=[{'label': c, 'value': c}
                                  for c in (poison['Race and Hispanic Origin'].unique())], className='dcc_compon'),


            html.Img(src=app.get_asset_url('nchslogo.jpeg'),
                     id='nchs-logo',
                     style={
                        "height": "100px",
                        "display": "block",
                        "margin": "auto",
                        "width": "auto",
                        "margin-top": "50px"
            },
            ),
            html.P('Data provided by NCHS', className='fix_label', style={'color': '#3065C9',
                                                                          'margin-top': '30px',
                                                                          'margin-bottom': '30px',
                                                                          'text-align': 'center'}),
        ], className="create_container2 three columns"),

        html.Div([
            dcc.Graph(id='bar_chart',
                      config={'displayModeBar': 'hover'}),

        ], className='create_container2 five columns'),

        html.Div([
            dcc.Graph(id='pie_chart1',
                      config={'displayModeBar': 'hover'}),

        ], className='create_container2 four columns'),

    ], className="row flex-display"),

), id="mainContainer", style={"display": "flex", "flex-direction": "column"})


@app.callback(Output('text3', 'children'),
              [Input('select_year', 'value'), Input('select_origin', 'value')])
def update_text(select_year, select_origin):
    poison8 = poison.groupby(['Year', 'Race and Hispanic Origin', 'Age'])[
        'Deaths'].sum().reset_index()
    poison9 = poison8[(poison8['Year'] == select_year) & (poison8['Race and Hispanic Origin'] == select_origin) &
                      (poison8['Age'] == '75+ years')]['Deaths'].sum()

    return [
        html.H6(children='75+ Years (Age)',
                style={'textAlign': 'center',
                       'color': 'rgb(50, 50, 50)'}
                ),

        html.P('{0:,.0f}'.format(poison9),
               style={'textAlign': 'center',
                      'color': '#3065C9',
                      'fontSize': 30}
               ),
    ]


@app.callback(Output('line_chart', 'figure'),
              [Input('select_year', 'value')])
def update_graph(select_year):
    poison8 = poison.groupby(['Year'])['Deaths'].sum().reset_index()

    return {
        'data': [go.Scatter(
            x=poison8['Year'],
            y=poison8['Deaths'],
            text=poison8['Deaths'],
            texttemplate='%{text:.2s}',
            textposition='bottom center',
            mode='markers+lines+text',
            line=dict(width=3, color='#30C9C7'),
            marker=dict(size=10, symbol='circle', color='#935cdb',
                        line=dict(color='#935cdb', width=2)
                        ),

            hoverinfo='text',
            hovertext='<b>Year</b>: ' + poison8['Year'].astype(str) + '<br>' +
            '<b>Total Deaths</b>: ' +
            [f'{x:,.0f}' for x in poison8['Deaths']] + '<br>'

        )],


        'layout': go.Layout(
            height=113,
            plot_bgcolor='#F2F2F2',
            paper_bgcolor='#F2F2F2',
            title={
                'text': 'Total Drug Poisoning Mortality from 1999 to 2015',

                'y': 0.96,
                'x': 0.7,
                'xanchor': 'right',
                'yanchor': 'top'},
            titlefont={
                'color': 'rgb(50, 50, 50)',
                'size': 15},

            hovermode='x',
            margin=dict(l=0, r=0, b=0, t=0),

            xaxis=dict(title='<b></b>',
                       visible=False,
                       color='#3065C9',
                       showline=True,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='black',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='#3065C9')

                       ),

            yaxis=dict(title='<b></b>',
                       visible=False,
                       color='#3065C9 ',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='black',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='#3065C9 ')

                       ),

            legend={
                'orientation': 'h',
                'bgcolor': '#F2F2F2',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font=dict(
                family="sans-serif",
                size=12,
                color='rgb(50, 50, 50)'),

        )

    }


@app.callback(Output('text1', 'children'),
              [Input('select_year', 'value'), Input('select_origin', 'value')])
def update_text(select_year, select_origin):
    poison4 = poison.groupby(['Year', 'Race and Hispanic Origin'])[
        'Deaths'].sum().reset_index()
    poison5 = poison4[(poison4['Year'] == select_year) & (
        poison4['Race and Hispanic Origin'] == select_origin)]['Deaths'].sum()

    return [
        html.H6(children='Deaths by Drug Poisonings',
                style={'textAlign': 'center',
                       'color': 'rgb(50, 50, 50)'}
                ),

        html.P('{0:,.0f}'.format(poison5),
               style={'textAlign': 'center',
                      'color': '#3065C9',
                      'fontSize': 32}
               ),
    ]


@app.callback(Output('text2', 'children'),
              [Input('select_year', 'value'), Input('select_origin', 'value')])
def update_text(select_year, select_origin):
    poison6 = poison.groupby(['Year', 'Race and Hispanic Origin', 'Age'])[
        'Deaths'].sum().reset_index()
    poison7 = poison6[(poison6['Year'] == select_year) & (poison6['Race and Hispanic Origin'] == select_origin) & (
        poison6['Age'] == '14 or less')]['Deaths'].sum()

    return [
        html.H6(children='14 or less (Age)',
                style={'textAlign': 'center',
                       'color': 'rgb(50, 50, 50)'}
                ),

        html.P('{0:,.0f}'.format(poison7),
               style={'textAlign': 'center',
                      'color': '#3065C9',
                      'fontSize': 30}
               ),
    ]


@app.callback(Output('bar_chart', 'figure'),
              [Input('select_year', 'value'), Input('select_origin', 'value')])
def update_graph(select_year, select_origin):
    poison1 = poison.groupby(['Year', 'Race and Hispanic Origin', 'Age'])[
        'Deaths'].sum().reset_index()

    poison2 = poison1[(poison1['Year'] == select_year) & (poison1['Race and Hispanic Origin'] == select_origin)].sort_values(
        by=['Age'], ascending=True)

    return {
        'data': [go.Bar(
            x=poison2[(poison2['Year'] == select_year) & (
                poison2['Race and Hispanic Origin'] == select_origin)]['Deaths'],
            y=poison2[(poison2['Year'] == select_year) & (
                poison2['Race and Hispanic Origin'] == select_origin)]['Age'],
            text=poison2[(poison2['Year'] == select_year) & (
                poison2['Race and Hispanic Origin'] == select_origin)]['Deaths'],
            texttemplate='Total deaths: ' + '%{text:.2s}',
            textposition='auto',
            orientation='h',
            marker=dict(color='#19AAE1 '),

            hoverinfo='text',
            hovertext='<b>Year</b>: ' + poison2[poison2['Year'] == select_year]['Year'].astype(str) + '<br>' +
            '<b>Age</b>: ' + poison2[poison2['Year'] == select_year]['Age'] + '<br>' +
            '<b>Total Deaths</b>: ' +
            [f'{x:,.0f}' for x in poison2[poison2['Year']
                                          == select_year]['Deaths']] + '<br>'

        )],


        'layout': go.Layout(
            plot_bgcolor='#F2F2F2',
            paper_bgcolor='#F2F2F2',
            title={
                'text': 'Total Deaths by Age Group in Year' + ' ' + str((select_year)),

                'y': 0.96,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': 'rgb(50, 50, 50)',
                'size': 20},

            hovermode='x',
            margin=dict(l=130),

            xaxis=dict(title='<b>Deaths</b>',
                       color='#3065C9 ',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='black',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='#3065C9 ')

                       ),

            yaxis=dict(title='<b></b>',
                       autorange='reversed',
                       color='#3065C9 ',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='black',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Arial',
                           size=12,
                           color='#3065C9 ')

                       ),

            legend={
                'orientation': 'h',
                'bgcolor': '#F2F2F2',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font=dict(
                family="sans-serif",
                size=12,
                color='rgb(50, 50, 50)'),

        )

    }


@app.callback(Output('pie_chart1', 'figure'),
              [Input('select_year', 'value'), Input('select_origin', 'value')])
def update_graph(select_year, select_origin):
    poison3 = poison.groupby(['Year', 'Race and Hispanic Origin', 'Sex'])[
        'Deaths'].sum().reset_index()
    male_deaths = poison3[(poison3['Year'] == select_year) & (poison3['Race and Hispanic Origin'] == select_origin) & (
        poison3['Sex'] == 'Male')]['Deaths'].sum()
    female_deaths = poison3[(poison3['Year'] == select_year) & (poison3['Race and Hispanic Origin'] == select_origin) & (
        poison3['Sex'] == 'Female')]['Deaths'].sum()
    colors = ['#60adeb', '#935cdb']

    return {
        'data': [go.Pie(labels=['Male', 'Female'],
                        values=[male_deaths, female_deaths],
                        marker=dict(colors=colors),
                        hoverinfo='label+value+percent',
                        textinfo='label+value',
                        textfont=dict(size=13),
                        texttemplate='%{label}: %{value} <br>(%{percent})',
                        textposition='auto',

                        )],

        'layout': go.Layout(
            plot_bgcolor='#F2F2F2',
            paper_bgcolor='#F2F2F2',
            hovermode='x',
            title={
                'text': 'Total Deaths by Sex in Year' + ' ' + str((select_year)),

                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': 'rgb(50, 50, 50)',
                'size': 20},
            legend={
                'orientation': 'h',
                'bgcolor': '#F2F2F2',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},

            font=dict(
                family="sans-serif",
                size=12,
                color='rgb(50, 50, 50)')
        ),

    }


if __name__ == '__main__':
    app.run_server(debug=True)
