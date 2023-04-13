                                                            Build a Dashboard Application with Plotly Dash
								    in this lab, we will be building a Plotly Dash application for users to perform interactive visual analytics 
							                                            	on SpaceX launch data in real-time.
#import necessery laibreries
import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
from dash import html
from dash import Input
from dash import Output


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()



# creat Dash app
app=dash.Dash(__name__)
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[{'label':'All Sites','value':'All'},
                                                                          {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                                                          {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                                                          {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                                                          {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'}],
                                            value='All',searchable=True,placeholder="Select a Launch Site"),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                 min=0,
                                                max=10000,
                                                step=1000,
                                               value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown',component_property='value')
             )

#creat pie chart to show the total successful launches count for all sites
# If a specific launch site was selected, show the Success vs. Failed counts for the site
def get_pie_chart(entered_value):
    if entered_value=="All":
        pie_fig=px.pie(spacex_df,
                   names="Launch Site",values="class",
                   color="Launch Site",
                   title="Total Success Launches By Site")
        return pie_fig
    else:
        Site_class=spacex_df[["Launch Site","class"]].value_counts().to_frame().reset_index().rename(columns={0:"Count"})
        Site_class_df=Site_class[Site_class["Launch Site"]==entered_value]
        pie_fig=px.pie(Site_class_df,
                   names="class",values="Count",
                   color="class",
                   title=f'Successed vs failed Launches in {entered_value} site')
        return pie_fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
                Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])

# creat a scatter chart to show the correlation between payload and launch success.
def get_scatter_chart(entered_value, payload_mass=[0,10000]):
    if entered_value == 'All':
        new_df = spacex_df[spacex_df["Payload Mass (kg)"]>=payload_mass[0]]
        new_df1 = new_df[new_df["Payload Mass (kg)"]<=payload_mass[1]]
        fig2 = px.scatter(new_df1, y="class", x="Payload Mass (kg)", 
        color= "Booster Version Category", 
        title="Correlation between Payload Mass (Kg) and Launch Outcome")
    else:
        new_df = spacex_df[spacex_df["Launch Site"]==entered_value]
        new_df1 = new_df[new_df["Payload Mass (kg)"]>=payload_mass[0]]
        new_df2 = new_df1[new_df["Payload Mass (kg)"]<=payload_mass[1]]
        fig2 = px.scatter(new_df2, y="class", x="Payload Mass (kg)", 
        color="Booster Version Category", 
        title="Correlation between Payload Mass (Kg) and Launch Outcome")
    return fig2   


# run the app.

if __name__=="__main__":
    app.run_server()
else :
    print("erorr!")
