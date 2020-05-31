
# coding: utf-8

# In[8]:


import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
import plotly.express as px
import numpy as np

from geopy.geocoders import Nominatim


# In[9]:


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
                       'country']

    df = df[keepcolumns]
    df.columns = ['Number_of_positive_cases',
                     'Cumulative_number_of_positive_cases',
                     'Number_of_deaths',
                     'Cumulative_number_of_deaths',
                     'country']


    return df


# In[10]:


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
    return map_dataset


# In[11]:


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
    df= df[df.country.isin([country_name])]

    if not df.index.is_monotonic:
        df = df.sort_index()
    if df.shape[0]==0:
        print('The is no data with this country and dates')
    # output clean csv file
    return df


# In[12]:


def return_figures(dataset,df):
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    country =df.country.unique()[0]

   # first chart plot
   # as a line chart
    graph_one = []
    graph_one.append(
          go.Scatter(
          y = df.Number_of_positive_cases.tolist(),
          x = df.index.tolist(),
          mode = 'lines',
          name = country,
          line=dict(color='red', width=1)
          )
      )

    layout_one = dict(xaxis = dict( autotick=True),
                    yaxis = dict(title = 'Number of positive cases'),
                    autosize=True,
                    height=380,
                    margin=dict(
                        l=50,
                        r=50,
                        b=50,
                        t=60,
                        pad=4
                    ),
                    paper_bgcolor="lightskyblue",
                    title={
                            'text': "Number of positive cases (per day)"+' in <br>'+country,
                            'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'below',
                             'font': { 'family': 'Tahoma',
                                        'size': 13
                                    }
                                },
                            )

    # second chart plot
    graph_two = []
    graph_two.append(
      go.Scatter(
      y = df.Cumulative_number_of_positive_cases.tolist(),
      x = df.index.tolist(),
      mode = 'lines',
      line=dict(color='red', width=1),
      )
    )

    layout_two = dict(xaxis = dict( autotick=True),
                     yaxis = dict(title = 'Cumulative number of positive cases'),
                     autosize=True,
                     height=380,
                     margin=dict(
                                 l=50,
                                 r=50,
                                 b=50,
                                 t=60,
                                 pad=4
                                 ),
                     paper_bgcolor="lightskyblue",
                     title={ 'text': "Cumulative number of positive cases (per day)"+' in <br>'+country,
                             'y':0.9,
                             'x':0.5,
                             'xanchor': 'center',
                             'yanchor': 'below',
                              'font': { 'family': 'Tahoma',
                                         'size': 13
                                      }
                             },
                        )



    # third chart plot
    graph_three = []
    graph_three.append(
          go.Scatter(
          y = df.Number_of_deaths.tolist(),
          x = df.index.tolist(),
          mode = 'lines',
          line=dict(color='red', width=1),
          )
      )

    layout_three = dict(xaxis = dict(autotick=True),
                        yaxis = dict(title = 'Number of deaths'),
                        autosize=True,
                        height=380,
                        margin=dict(
                                    l=50,
                                    r=50,
                                    b=50,
                                    t=60,
                                    pad=4
                                    ),
                        paper_bgcolor="lightskyblue",
                        title={ 'text': "Number of deaths (per day)"+' in <br>'+country,
                                'y':0.9,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'below',
                                 'font': { 'family': 'Tahoma',
                                            'size': 13
                                         }
                                },


                )

    # fourth chart
    graph_four = []

    graph_four.append(
          go.Scatter(
          y = df.Cumulative_number_of_deaths.tolist(),
          x = df.index.tolist(),
          mode = 'lines',
          line=dict(color='red', width=1),
          )
      )

    layout_four = dict(xaxis = dict(autotick=True),
                       yaxis = dict(title = 'Cumulative number of deaths'),
                       autosize=True,
                       height=380,
                       margin=dict(
                                   l=50,
                                   r=50,
                                   b=50,
                                   t=60,
                                   pad=4
                                   ),
                        paper_bgcolor="lightskyblue",
                        title={ 'text': "Cumulative number of deaths (per day)" +' in <br>'+country,
                                'y':0.9,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'below',
                                'font': { 'family': 'Tahoma',
                                          'size': 13
                                         }
                              },
                        )
    # fifth chart
    graph_five = []



    graph_five.append(go.Scattermapbox( lat=dataset.latitude.tolist(),
                        lon=dataset.longitude.tolist(),
                        mode='markers',
                        hoverinfo='text',
                        text = ['Cumulative number of positive cases:  {} <br> Cumulative number of deaths:  {}<br> Country:  {}'.format(dataset[dataset.columns[[1,3,4]]].values[i][0],dataset[dataset.columns[[1,3,4]]].values[i][1],dataset[dataset.columns[[1,3,4]]].values[i][2])
                                                for i in range(dataset.shape[0])],
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


# In[13]:


if __name__=='__main__':

    dataset = get_dataset()
    map_data = set_map_data(dataset)

    fig = go.Figure(px.scatter_mapbox(
                              data_frame=map_data,
                              lat='latitude',
                              lon='longitude',
                              hover_name='country',
                              hover_data=map_data.columns[[1,3]],
                              color_discrete_sequence=["fuchsia"],
                              zoom=3,
                              height=300,
                            )
                          )



    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox=go.layout.Mapbox(
        style="stamen-terrain",

        )
    )

    fig.show()

    df = filter_data(dataset, country_name = 'Iran', date = [dataset.index.min(), dataset.index.max()])

    plt.figure(figsize = [12,5])

    #ax.plot(df.cases)
    ax = plt.subplot(1,2,1)
    plt.plot(df.Number_of_positive_cases)
    plt.xticks(Rotation=90);

    every_nth = 10
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)

    ax = plt.subplot(1,2,2)
    plt.plot(df.Cumulative_number_of_positive_cases)
    plt.xticks(Rotation=90);

    every_nth = 10
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)

    plt.figure(figsize = [12,5])

    #ax.plot(df.cases)
    ax = plt.subplot(1,2,1)
    plt.plot(df.Number_of_deaths)
    plt.xticks(Rotation=90);

    every_nth = 10
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)

    ax = plt.subplot(1,2,2)
    plt.plot(df.Cumulative_number_of_deaths)
    plt.xticks(Rotation=90);

    every_nth = 10
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
