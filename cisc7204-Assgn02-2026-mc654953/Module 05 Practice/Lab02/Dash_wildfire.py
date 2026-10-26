# -*- coding: utf-8 -*-
"""
CISC7204 Assignment 02 - Module 05 Practice Project - Part 2
Creating Dashboards: Australia Wildfire Dashboard
CISC7204 Assgn02 Module 05 - PracticeProjLab02
mc654953 Fong Hoi Lam, mc653748 Fong Chin Wai
"""

import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Create a dash application
app = dash.Dash(__name__)
server = app.server

# Dataset: Historical Wildfires (Australia)
df = pd.read_csv('Historical_Wildfires.csv')

# Data processing: extract Month name and Year from Date
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Layout of the dashboard
app.layout = html.Div(children=[
    html.H1('Australia Wildfire Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 26}),

    # Outer division for the layout
    html.Div([
        # First inner division: inputs (RadioItems + Dropdown)
        html.Div([
            html.H2('Select Region:', style={'margin-right': '2em'}),
            dcc.RadioItems(
                options=[
                    {'label': 'New South Wales', 'value': 'NSW'},
                    {'label': 'Northern Territory', 'value': 'NT'},
                    {'label': 'Queensland', 'value': 'QL'},
                    {'label': 'South Australia', 'value': 'SA'},
                    {'label': 'Tasmania', 'value': 'TA'},
                    {'label': 'Victoria', 'value': 'VI'},
                    {'label': 'Western Australia', 'value': 'WA'}
                ],
                value='NSW',
                id='region',
                inline=True
            ),
            html.H2('Select Year:', style={'margin-right': '2em'}),
            dcc.Dropdown(df.Year.unique(), value=2005, id='year')
        ], style={'width': '30%', 'display': 'inline-block'}),

        # Second inner division: output plots
        html.Div([
            html.Div([], id='plot1'),
            html.Div([], id='plot2')
        ], style={'display': 'flex'})
    ])
])

# Callback: update both plots based on selected region and year
@app.callback([
    Output(component_id='plot1', component_property='children'),
    Output(component_id='plot2', component_property='children')
], [
    Input(component_id='region', component_property='value'),
    Input(component_id='year', component_property='value')
])
def reg_year_display(input_region, input_year):
    # Filter data by region and year
    region_data = df[df['Region'] == input_region]
    y_r_data = region_data[region_data['Year'] == input_year]

    # Pie chart: monthly average estimated fire area
    est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(est_data, values='Estimated_fire_area', names='Month',
                  title="{} : Monthly Average Estimated Fire Area in year {}".format(input_region, input_year))

    # Bar chart: monthly average count of pixels for presumed vegetation fires
    veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(veg_data, x='Month', y='Count',
                  title='{} : Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(input_region, input_year))

    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]


# Run the application
if __name__ == '__main__':
    # Dash 4.x: app.run() replaces the deprecated app.run_server()
    app.run(debug=True)
