
# coding: utf-8

# In[1]:


import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
import plotly.express as px
import numpy as np

# In[2]:


def get_dataset():
    """POST to API to get the dataset"""

    payload ={'code': "ALL"}# {'country': 'United States of America'}
    URL = 'https://api.statworx.com/covid'
    response = requests.post(url=URL, data=json.dumps(payload))

    # Convert to data frame
    df = pd.DataFrame.from_dict(json.loads(response.text))
    df.set_index('date',inplace=True)



    # Keep only the columns of interest
    keepcolumns = ['cases','cases_cum','deaths','deaths_cum',
                       'country','code']

    df = df[keepcolumns]
    df.columns = ['Number_of_positive_cases',
                     'Cumulative_number_of_positive_cases',
                     'Number_of_deaths',
                     'Cumulative_number_of_deaths',
                     'country','code']


    return df


# In[3]:


def set_map_data(dataset):

    coordinates = pd.read_csv('./data/coordinates.csv' ,index_col=0)
    coordinates = coordinates.groupby('country')['longitude','latitude'].agg(['unique'])
    coordinates.columns = coordinates.columns.droplevel(1)
    coordinates['longitude']=coordinates.longitude.apply(lambda x: x[0])#
    coordinates['latitude']=coordinates.latitude.apply(lambda x: x[0])#
    coordinates.reset_index(inplace=True)
    dataset.reset_index(inplace=True)
    map_dataset = dataset.merge(coordinates, left_on='country', right_on='country')
    map_dataset = map_dataset.set_index(pd.DatetimeIndex(map_dataset['date']))
    map_dataset=map_dataset[map_dataset.groupby('country')['date'].transform('max') == map_dataset['date']]
    map_dataset.drop(columns='date',inplace=True)
    dataset.set_index('date',inplace=True)

    return map_dataset


# In[4]:


def filter_data(dataset, country_name = 'United_States_of_America', date = ['2019-12-31', '2020-05-29']):
    """filter Covid data for a visualizaiton dashboard

    Keeps data range of dates in country variable


    Args:
        dataset (str): name of the csv data file
        country name (str): name of the country
        dates (date tuple string ):  start date and final date in form of ('2019-12-31','2020-01-31') to Keep data range of dates

    Returns:
        data frame

    """
    df = dataset.loc[(dataset.index>=date[0]) & (dataset.index <=date[1])]
    df= df[df.country.isin(country_name)]

    if not df.index.is_monotonic:
        df = df.sort_index()
    if df.shape[0]==0:
        print('The is no data with this country and dates')
    # output clean csv file
    return df


# In[5]:


def get_the_top(map_dataset):
    # get list of the five top countries and all countrie

    map_dataset.sort_values('Cumulative_number_of_deaths',ascending=False,inplace=True)


    codes = map_dataset.iloc[:5].country.values
    countries = map_dataset.iloc[:5].code.values

    country_default = []
    [country_default.append((country, code)) for code, country in zip(countries,codes)];

    country_codes =[]
    [country_codes.append([country, code]) for  country,code in zip(map_dataset.country.tolist(),map_dataset.code.tolist())];

    return country_default, country_codes


# In[6]:


def return_figures(map_dataset,df):
    """Creates four plotly visualizations

    Args:
        map_dataset DataFrame
        filter dataset DataFrame

    Returns:
        list (dict): list containing the five plotly visualizations

    """


   # first chart plot
   # as a line chart
    graph_one = []
    for country in df.country.unique():
        graph_one.append(go.Scatter(
                         x = df[df['country'] == country].index.tolist(),
                         y = df[df['country'] == country].Number_of_positive_cases.tolist(),
                         mode = 'lines',
                         name = str(country),
                         line=dict(width=1),
                         hovertemplate='Date: %{x}  <br> Positive cases: %{y}  ',
                                )
                         )



    layout_one = dict(xaxis = dict( autotick=True),
                    yaxis = dict(title = 'Number of positive cases',ticksuffix=" "),
                    autosize=True,
                    height=380,
                    hovermode ='closest' ,
                    margin=dict(
                        l=50,
                        r=20,
                        b=50,
                        t=60,
                        pad=.2
                    ),
                    paper_bgcolor="lightskyblue",
                    title={
                            'text': "<b>Number of positive cases (per day)</b>",
                            'y':0.91,
                            'x':0.55,
                            'xanchor': 'center',
                            'yanchor': 'below',
                            'font': { 'family': 'Tahoma',
                                      'size': 12
                                     }
                          },
                    showlegend=True,
                    legend=dict(x=0, y=1, bgcolor='rgba(0,0,0,0)',  font=dict( family="sans-serif", size=11, color="black")),
                    )

    # second chart plot
    graph_two = []
    for country in df.country.unique():
        graph_two.append(go.Scatter(
                         y = df[df['country'] == country].Cumulative_number_of_positive_cases.tolist(),
                         x =df[df['country'] == country].index.tolist(),
                         mode = 'lines',
                         line=dict(width=1),
                         name = str(country),
                         hovertemplate='Date: %{x}  <br> Cum positive cases: %{y}  ',
                                   )
                        )

    layout_two = dict(xaxis = dict( autotick=True),
                     yaxis = dict(title = 'Cumulative number of positive cases'),
                     autosize=True,
                    height=380,
                     hovermode ='closest' ,
                     margin=dict(
                                 l=50,
                                 r=20,
                                 b=50,
                                 t=60,
                                 pad=.2
                                 ),
                     paper_bgcolor="lightskyblue",
                     title={ 'text': "<b>Cumulative number of positive cases</b>",
                             'y':0.91,
                             'x':0.55,
                             'xanchor': 'center',
                             'yanchor': 'below',
                              'font': { 'family': 'Tahoma',
                                        'size': 12
                                      }
                             },
                        showlegend=True,
                        legend=dict(x=0, y=1, bgcolor='rgba(0,0,0,0)',  font=dict( family="sans-serif", size=11, color="black")),
                        )



    # third chart plot
    graph_three = []
    for country in df.country.unique():
        graph_three.append(go.Scatter(
                           y = df[df['country'] == country].Number_of_deaths.tolist(),
                           x = df[df['country'] == country].index.tolist(),
                           mode = 'lines',
                           line=dict(width=1),
                           name = str(country),
                           hovertemplate='Date: %{x}  <br> Number of deaths: %{y}  ',

                                      )
                          )

    layout_three = dict(xaxis = dict(autotick=True),
                        yaxis = dict(title = 'Number of deaths'),
                        autosize=True,
                        height=380,
                        hovermode ='closest' ,
                        margin=dict(
                                    l=50,
                                    r=10,
                                    b=50,
                                    t=60,
                                    pad=.2
                                    ),
                        paper_bgcolor="lightskyblue",
                        title={ 'text': "<b>Number of deaths (per day) </b>",
                                'y':0.91,
                                'x':0.55,
                                'xanchor': 'center',
                                'yanchor': 'below',
                                 'font': { 'family': 'Tahoma',
                                            'size': 12
                                         }
                                },
                        showlegend=True,
                        legend=dict(x=0, y=1, bgcolor='rgba(0,0,0,0)',  font=dict( family="sans-serif", size=11, color="black")),

                                        )

    # fourth chart
    graph_four = []
    for country in df.country.unique():
        graph_four.append(go.Scatter(
                          y = df[df['country'] == country].Cumulative_number_of_deaths.tolist(),
                          x = df[df['country'] == country].index.tolist(),
                          mode = 'lines',
                          line=dict(width=1),
                          name = str(country),
                          hovertemplate='Date: %{x}  <br> Cum number of deaths: %{y}  ',

                          )
                      )

    layout_four = dict(xaxis = dict(autotick=True),
                       yaxis = dict(title = 'Cumulative number of deaths',ticksuffix=" "),
                       autosize=True,
                       height=380,
                       hovermode ='closest' ,
                       margin=dict(
                                   l=50,
                                   r=20,
                                   b=50,
                                   t=60,
                                   pad=.2
                                   ),
                        paper_bgcolor="lightskyblue",
                        title={ 'text': "<b>Cumulative number of deaths </b>",
                                'y':.91,
                                'x':0.55,
                                'xanchor': 'center',
                                'yanchor': 'below',
                                'font': { 'family': 'Tahoma',
                                          'size': 12
                                         }
                              },
                        showlegend=True,
                        legend=dict(x=0, y=1, bgcolor='rgba(0,0,0,0)',  font=dict( family="sans-serif", size=11, color="black")),

                        )
    # fifth chart
    graph_five = []



    graph_five.append(go.Scattermapbox( lat=map_dataset.latitude.tolist(),
                        lon=map_dataset.longitude.tolist(),
                        mode='markers',
                        hoverinfo='text',
                        text = ['Cumulative number of positive cases:  {} <br> Cumulative number of deaths:  {}<br> Country:  {}'.format(map_dataset[map_dataset.columns[[1,3,4]]].values[i][0],map_dataset[map_dataset.columns[[1,3,4]]].values[i][1],map_dataset[map_dataset.columns[[1,3,4]]].values[i][2])
                                                for i in range(map_dataset.shape[0])],
                        marker=go.scattermapbox.Marker(
                                            size=5,
                                            color="fuchsia",
                                            opacity=0.7
                                                    ),
                                    )
                    )



    layout_five = dict( hovermode='closest',
                        mapbox=dict(
                        accesstoken='pk.eyJ1IjoiYW1pcnppYWVlIiwiYSI6ImNrYXNlZXd4eDBpcXAzMG1zOTR1NWt2bzUifQ.9vOmF1-LoxDggkQshH6sbQ',
                        bearing=0,
                        pitch=0,
                        zoom=0),
                        mapbox_style="stamen-terrain",
                        margin=dict(
                                l=50,
                                r=50,
                                b=50,
                                t=60,
                                pad=4
                                    ),
                        paper_bgcolor="powderblue",
                        )





    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five, layout=layout_five))


    return figures


# In[7]:


if __name__=='__main__':

    dataset = get_dataset()
    map_data = set_map_data(dataset)

    fig =go.Figure(go.Scattermapbox(lat=map_data.latitude.tolist(),
                                    lon=map_data.longitude.tolist(),
                                    mode='markers',
                                    hoverinfo='text',
                                    text = ['Cumulative number of positive cases:  {} <br> Cumulative number of deaths:  {}<br> Country:  {}'.format(map_data[map_data.columns[[1,3,4]]].values[i][0],map_data[map_data.columns[[1,3,4]]].values[i][1],map_data[map_data.columns[[1,3,4]]].values[i][2])
                                                            for i in range(map_data.shape[0])],

                                    marker=go.scattermapbox.Marker(
                                                        size=5,
                                                        color="fuchsia",
                                                        opacity=0.7
                                                                   ),

                                            )
                  )


    fig.update_layout(title = 'The global outbreak of COVID-19',
                    hovermode='closest',
                    mapbox=dict(
                    accesstoken='pk.eyJ1IjoiYW1pcnppYWVlIiwiYSI6ImNrYXNlZXd4eDBpcXAzMG1zOTR1NWt2bzUifQ.9vOmF1-LoxDggkQshH6sbQ',
                    bearing=0,
                    pitch=0,
                    zoom=3),
                    mapbox_style="stamen-terrain",)
    fig.show()

    country_default, country_codes = get_the_top(map_data)
    country_default = [country for country, code in country_default]
    dates=[dataset.index.min(), dataset.index.max()]

    df = filter_data(dataset, country_name = country_default, date = dates  )

    fig = go.Figure()
    for country in df.country.unique():
        fig.add_traces(go.Scatter(
                         y = df[df['country'] == country].Cumulative_number_of_positive_cases.tolist(),
                         x =df[df['country'] == country].index.tolist(),
                         mode = 'lines',
                         line=dict( width=1),
                         name=str(country),

                                    )
                        )

    fig.show()
