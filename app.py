from dash import Dash, dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go

import numpy as np
from numpy import array
import pandas as pd
import glob
import os
import json

from os import listdir
from os.path import isfile, join

import analysis

# Get patient's personal data

profile_file = glob.glob('/Users/georgia/Documents/Thesis/geobot/profile.json')
profile_file = max(profile_file, key=os.path.getctime)

with open(profile_file) as json_file:
    for line in json_file:
        data = json.loads(line.strip())

first_name = data['first_name']
last_name = data['last_name']
age = data['age']
sex = data['sex']
cur_med = data['cur_med']

if cur_med is None:
    cur_med = "-"
else:
    cur_med=cur_med

logs_path = '/Users/georgia/Documents/Thesis/geobot/logs'
files = [f for f in listdir(logs_path) if isfile(join(logs_path, f))]
if '.DS_Store' in files:
    files.remove('.DS_Store')
files = sorted(files, reverse = True)

wellness_logs_path = '/Users/georgia/Documents/Thesis/geobot/wellness_form_logs'
wellness_files = [f for f in listdir(wellness_logs_path) if isfile(join(wellness_logs_path, f))]
if '.DS_Store' in wellness_files:
    wellness_files.remove('.DS_Store')
wellness_files = sorted(wellness_files, reverse = True)

mental_logs_path = '/Users/georgia/Documents/Thesis/geobot/mental_form_logs'
mental_files = [f for f in listdir(mental_logs_path) if isfile(join(mental_logs_path, f))]
if '.DS_Store' in mental_files:
    mental_files.remove('.DS_Store')
mental_files = sorted(mental_files, reverse = True)


default_value_conv = files[0]
controls_date = dbc.FormGroup(
    [
        html.P('Choose Date'),
        dcc.Dropdown(
            className='dropdown',
            id='dropdown_conv',
            options=[{'label':date[4:-5],'value':date} for date in files],
            value=default_value_conv,  # default value
            multi=False,
            style={
            'margin':'auto',
            # 'textAlign':'center'
            }
        )
    ]
)

default_value_wellness = wellness_files[0]
controls_wellness = dbc.FormGroup(
    [
        html.P('Choose Date'),
        dcc.Dropdown(
            className='dropdown',
            id = 'dropdown_wellness',
            options=[{'label':date[4:-5],'value':date} for date in wellness_files],
            value=default_value_wellness,  # default value
            multi=False,
            style={
            'margin':'auto',
            # 'textAlign':'center'
            }
        )
    ]
)

default_value_mental = mental_files[0]
controls_mental = dbc.FormGroup(
    [
        html.P('Choose Date'),
        dcc.Dropdown(
            className='dropdown',
            id='dropdown_mental',
            options=[{'label':date[7:-5],'value':date} for date in mental_files],
            value=default_value_mental,  # default value
            multi=False,
            style={
            'margin':'auto',
            # 'textAlign':'center'
            }
        )
    ]
)

sidebar = html.Div(
    [
        html.H2('Conversations', className='sidebar_heading'),
        html.Hr(className='sidebar_hr'),
        controls_date,
        html.Br(),
        html.H2('Wellness form', className='sidebar_heading'),
        html.Hr(className='sidebar_hr'),
        controls_wellness,
        html.Br(),
        html.H2('Mental Health form', className='sidebar_heading'),
        html.Hr(className='sidebar_hr'),
        controls_mental,
    ],
    className="sidebar",
)

# Table - Show patient's personal data

profile_table_header = [
    html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name"), html.Th("Age"), html.Th("Sex"), html.Th("Medication")], className="main_table"))
]

row = html.Tr([html.Td(first_name), html.Td(last_name), html.Td(age), html.Td(sex), html.Td(cur_med)], className="main_table")

profile_table_body = [html.Tbody(row)]

profile_table = dbc.Table(profile_table_header + profile_table_body)

# Show graph with emotions throughout the conversation

emotion_graph = dbc.Row(
    [
        dbc.Col(dcc.Graph(id='graph'))
    ]
)

# Print out patient's peaks, lows, average sentiment

min_header = [html.Thead(html.Tr([html.Th("Minimum emotion"), html.Th("Message")], className='report_table_min'))]
min_row = [html.Tr([html.Td(id='report_table_min_emo'), html.Td(id='report_table_min_emo_msg')], className='report_table_min')]
min_body = [html.Tbody(min_row)]
min_table = dbc.Table(min_header + min_body)

max_header = [html.Thead(html.Tr([html.Th("Maximum emotion"), html.Th("Message")], className='report_table_max'))]
max_row = [html.Tr([html.Td(id='report_table_max_emo'), html.Td(id='report_table_max_emo_msg')], className='report_table_max')]
max_body = [html.Tbody(max_row)]
max_table = dbc.Table(max_header + max_body)

avg_header = [html.Thead(html.Tr([html.Th("Average emotion"), html.Th("")], className='report_table_avg'))]
avg_row = [html.Tr([html.Td(id='report_table_avg_emo'), html.Td()], className='report_table_avg')]
avg_body = [html.Tbody(avg_row)]
avg_table = dbc.Table(avg_header + avg_body)

# Table - Show patient's wellness form data

params = ["Date", "Exercise", "Sleep", "Diet", "Medication", "Stress Level", "Goal"]
ids = ["date", "exercise", "sleep", "diet", "medication", "stress", "goal"]

wellness_table = html.Div([
    dash_table.DataTable(
        id='wellness_table',
        columns=([{'id': i, 'name': p} for p,i in zip(params,ids)]),
        virtualization=True,
        fixed_rows={'headers': True},
        style_header={
            'textAlign':'center',
            'fontFamily':'Helvetica Neue',
            'fontWeight':'bold',
            'color': '#4646a3'
        },
        style_cell={
            'textAlign':'center',
            'fontFamily':'Helvetica Neue',
            'padding':'10px 10px',
            'width': 255
        },
        style_table={
            'height': 500
        }
    )
])

# Table - Show patient's mental health form data

mental_params = ["Date", "Little interest in doing things", "Feeling down, depressed", "Trouble sleeping or over-sleeping", "Feeling tired or having little energy", "Poor appetite or overeating", "Feeling bad about yourself", "Trouble concentrating on things", "Thoughts of hurting yourself"]
mental_ids = ["date", "mentalq1", "mentalq2", "mentalq3", "mentalq4", "mentalq5", "mentalq6", "mentalq7", "mentalq8"]

mental_table = html.Div([
    dash_table.DataTable(
        id='mental_table',
        columns=([{'id': i, 'name': p} for p,i in zip(mental_params,mental_ids)]),
        virtualization=True,
        fixed_rows={'headers': True},
        style_header={
            'textAlign':'center',
            'fontFamily':'Helvetica Neue',
            'fontWeight':'bold',
            'color': '#4646a3'
        },
        style_cell={
            'textAlign':'center',
            'fontFamily':'Helvetica Neue',
            'padding':'10px 10px',
            'width': 255
        },
        style_table={
            'height': 500
        }
    )
])

# Page 1 Content Layout

page_1_content = html.Div(
    [
        html.H2('Emotion Analytics', className='page_heading'),
        html.Br(),
        profile_table,
        html.Br(),
        html.H3('Emotions Graph throughout conversation', id='emo_graph_heading'),
        emotion_graph,
        html.H3('Analytic Report', className='report_heading'),
        min_table,
        max_table,
        avg_table,
        html.Br()
    ],
    className="content"
)

# Page 2 Content Layout

page_2_content = html.Div(
    [
        html.H2('Wellness Form', className='page_heading'),
        html.Br(),
        profile_table,
        html.Br(),
        html.H3('Weekly Report', className='report_heading'),
        wellness_table
    ],
    className="content"
)

#Page 3 Content Layout

page_3_content = html.Div(
    [
        html.H2('Mental Health Form', className='page_heading'),
        html.Br(),
        profile_table,
        html.Br(),
        html.H3('Weekly Report', className='report_heading'),
        mental_table
    ],
    className="content",
    id='page_3_content'
)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

app.layout = html.Div([sidebar, html.Div(id='page_content')])

@app.callback(
    Output('page_content','children'),
    Output('dropdown_conv', 'value'),
    Output('dropdown_wellness', 'value'),
    Output('dropdown_mental','value'),
    [Input('dropdown_conv', 'value'),
    Input('dropdown_wellness', 'value'),
    Input('dropdown_mental','value')])

def change_layout(value1, value2, value3):
    global default_value_conv
    global default_value_wellness
    global default_value_mental
    if value2 != default_value_wellness:
        default_value_wellness = value2
        default_value_conv = None
        default_value_mental = None
        return page_2_content, None, value2, None
    elif value3 != default_value_mental:
        default_value_mental = value3
        default_value_wellness =  None
        default_value_conv =  None
        return page_3_content, None, None, value3
    default_value_conv = value1
    default_value_wellness = None
    default_value_mental = None
    return page_1_content, value1, None, None

@app.callback(
    Output('graph', 'figure'), 
    Output('report_table_min_emo','children'), 
    Output('report_table_max_emo','children'), 
    Output('report_table_avg_emo','children'),
    Output('report_table_avg_emo','class'),
    Output('report_table_min_emo_msg','children'), 
    Output('report_table_max_emo_msg','children'), 
    Input('dropdown_conv', 'value'))

def update_page_1(value):
    emotions = list()
    messages = list()

    with open(join(logs_path,value)) as json_file:
        for line in json_file:
            data = json.loads(line.strip())
            # print(data)
            emotions.append(data['compound'])
            messages.append(data['msg'])

    fig = px.line(emotions)
    fig.update_layout({
        'height': 600},
        yaxis_title='Emotion',
        xaxis_title='Conversation',
        showlegend=False,
        xaxis=dict(dtick=1),
        yaxis=dict(range=[-1,1])
    )

    min_emotion = min(emotions)
    max_emotion = max(emotions)

    avg_emotion = "{:.3f}".format(analysis.sentiment_weight2_avg(join(logs_path,value)))
    c = "red"
    if float(avg_emotion) > 0:
        c = "green"

    min_emotion_msg = [messages[i] for i in range(len(emotions)) if emotions[i]==min_emotion][0]
    max_emotion_msg = [messages[i] for i in range(len(emotions)) if emotions[i]==max_emotion][0]
    
    return fig, min_emotion, max_emotion, avg_emotion, c ,min_emotion_msg, max_emotion_msg 

@app.callback(
    Output('wellness_table', 'data'),
    Input('dropdown_wellness', 'value'))

def update_page_2(value):
    result = list()
    curr = wellness_files.index(value)
    for i in range(curr,curr+7):
        if(i>len(wellness_files)-1):
            break
        with open(join(wellness_logs_path,wellness_files[i])) as json_file:
            for line in json_file:
                data = json.loads(line.strip())

        data['date'] = wellness_files[i][4:-5]

        if data['exercise'] is None:
            data['exercise'] = "-"

        if data['confirm_medication'] is False:
            data['medication'] = "-"
        else:
            data['medication'] = cur_med
            
        result.append(data)

    return result

@app.callback(
    Output('mental_table', 'data'),
    Input('dropdown_mental', 'value'))

def update_page_3(value):
    result = list()
    curr = mental_files.index(value)
    for i in range(curr,curr+7):
        if(i>len(mental_files)-1):
            break
        with open(join(mental_logs_path,mental_files[i])) as json_file:
            for line in json_file:
                data = json.loads(line.strip())

        data['date'] = mental_files[i][7:-5]
        result.append(data)

    return result

if __name__ == '__main__':
    app.run_server(debug=True)
