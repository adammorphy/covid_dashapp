import altair as alt
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import datetime as dt


#today = '{}'.format(dt.date.today())

alt.data_transformers.disable_max_rows()

df = pd.read_csv('owid-covid-data.csv')

# Change data to datetimes
df['date']= df['date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))

# Get World Data
sample_df = df[df['location'].isin(['Canada', 
                                    'United States',
                                   'United Kingdom',
                                   'Netherlands',
                                   'Ireland',
                                   'Italy',
                                   'Australia',
                                    'China',
                                   'Europe',
                                   'Asia',
                                    'South America',
                                    'North America',
                                    'Africa',
                                    'Oceania',
                                   'World'])]

# set time marks
marks = {int(i):str(j) for i,j in zip(range(len(sample_df[sample_df['location'] == 'Canada'].date)), sample_df[sample_df['location'] == 'Canada']['date'])}


def plot_altair(value, y, location):


    if value is None:
        tmax = list(marks.keys())[-1]
        tmin = 0
        y_axis = 'new_cases'
        location = 'Canada'

    else:
        tmax = value[1]
        tmin = value[0]
        y_axis = y

    
    df = sample_df[sample_df['location'] == location][sample_df[sample_df['location'] == location]['date'] < marks.get(tmax)][sample_df[sample_df['location'] == location]['date'] > marks.get(tmin)]

    chart = alt.Chart(df).mark_circle(color = 'red').encode(
        x=alt.X('date', title = 'Date'), 
        y=alt.Y(y_axis)
    ).properties(
        height = 200,
        width = 700
    )
    return chart.to_html()

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])



app = Dash(__name__)
app.layout = html.Div([
        dcc.Dropdown(
            id='ycol', value='new_cases',
            options=[{'label': i, 'value': i} for i in ['new_cases',
                                                         'total_cases', 'total_deaths', 
                                                         'new_deaths',
                                                         'icu_patients', 'icu_patients_per_million',
                                                         'hosp_patients', 'hosp_patients_per_million',
                                                         'total_vaccinations', 'new_vaccinations',
                                                         'total_vaccinations_per_hundred', 'people_fully_vaccinated_per_hundred']],
            style={'border-width': '0', 'width': '60%', 'height': '40px', 'backgroundColor': 'white'}),

        dcc.Dropdown(
            id='location', value='Canada',
            options=[{'label': i, 'value': i} for i in ['Canada', 
                                                        'United States',
                                                        'United Kingdom',
                                                        'Netherlands',
                                                        'Ireland',
                                                        'Italy',
                                                        'Australia',
                                                        'China',
                                                        'Europe',
                                                        'Asia',
                                                        'South America',
                                                        'North America',
                                                        'Africa',
                                                        'Oceania',
                                                        'World']],
            style={'border-width': '0', 'width': '60%', 'height': '40px', 'backgroundColor': 'white'}),

        html.Iframe(
            id='scatter',
            srcDoc=plot_altair(value = [0, list(marks.keys())[-1]], y = 'new_cases', location = 'Canada'),
            style={'border-width': '0', 'width': '100%', 'height': '275px', 'backgroundColor': 'white'}),

        dcc.RangeSlider(id='xslider', 
                    min=1,
                    max=list(marks.keys())[-1],
                    step=10,
                    included=False,
                    tooltip={"placement": "bottom", "always_visible": True},
                    marks = None
                    ), 
        dcc.Markdown('''
            ### Displaying Dates
          '''
        ),
        html.Div(id='slider-output-container2'),
        html.Div(id='slider-output-container1')
                    
],  style={'border-width': '0', 'width': '60%', 'backgroundColor': 'white'})

@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xslider', 'value'),
    Input('ycol', 'value'),
    Input('location', 'value'))
def update_output(value, y, location):
    if value is None:
        value = []
        value.append(0)
        value.append(list(marks.keys())[-1])
    return plot_altair(value, y, location)


@app.callback(
    Output('slider-output-container2', 'children'),
    Input('xslider', 'value'))
def update_output(value):
    if value is None:
        value = []
        value.append(0)
        value.append(list(marks.keys())[-1])
    return 'From: {}'.format(marks.get(value[0]))

@app.callback(
    Output('slider-output-container1', 'children'),
    Input('xslider', 'value'))
def update_output(value):
    if value is None:
        value = []
        value.append(0)
        value.append(list(marks.keys())[-1])
    return 'To: {}'.format(marks.get(value[1]))



if __name__ == '__main__':
    app.run_server(debug=True)