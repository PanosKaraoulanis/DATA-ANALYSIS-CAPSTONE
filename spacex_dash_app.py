# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                 dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                        {'label': 'All Sites', 'value': 'ALL'},
                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                                        ],
                                                value='ALL',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                            ),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                # Function decorator to specify function input and output                                
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                    min=min_payload, max=max_payload, step=1000,
                                                    marks={i: str(i) for i in range(0, 10000 + 1, 1000)},
                                                    value=[0, 10000]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),                                          
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                                            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df.groupby("Launch Site")["class"].sum().reset_index()
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total successes from all Launch Sites')
        return fig
    else:
        site_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        filtered_site = site_df.groupby("class").size().reset_index(name='count')
        fig = px.pie(filtered_site, values='count', 
        names='class', 
        title=f'Success vs Failure for {entered_site}')
        return fig      
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site,mass):
    payload_list = [float(i) for i in mass]
    filtered_df = spacex_df[spacex_df["Payload Mass (kg)"].between(payload_list[0], payload_list[1])]
    if entered_site == 'ALL':
        fig1 = px.scatter(filtered_df, x="Payload Mass (kg)",y="class", 
        color="Booster Version Category", 
        title='Total successes from all Launch Sites')
        return fig1
    else:
        site_df=spacex_df[spacex_df["Launch Site"]==entered_site]
        fig1 = px.scatter(site_df, x="Payload Mass (kg)",y="class", 
        color="Booster Version Category", 
        title=(f'Total successes from {entered_site}'))
        return fig1

# Run the app
if __name__ == '__main__':
    app.run_server(port=8055)