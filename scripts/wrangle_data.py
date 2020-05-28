
# coding: utf-8

# In[165]:


import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly 
import plotly.graph_objs as go


# In[185]:


def get_dataset():
    """POST to API to get the dataset""" 
    
    payload ={'code': "ALL"}# {'country': 'United States of America'} 
    URL = 'https://api.statworx.com/covid'
    response = requests.post(url=URL, data=json.dumps(payload))

    # Convert to data frame
    df = pd.DataFrame.from_dict(json.loads(response.text))
    df.set_index('date',inplace=True)
    
    # Keep only the columns of interest 
    keepcolumns = ['cases','cases_cum','deaths','deaths_cum','country']
    df = df[keepcolumns]
    
    return df


# In[214]:





# In[191]:


def filter_data(dataset, country_name = 'United_States_of_America', date = [dataset.index.min(), dataset.index.max()]):
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
    df.columns = ['Number_of_positive_cases',
                 'Cumulative_number_of_positive_cases',
                 'Number_of_deaths',
                 'Cumulative_number_of_deaths',
                 'country']

    # output clean csv file
    return df


# In[215]:


def return_figures(df):
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
    
    x_val =  df.Number_of_positive_cases.tolist()
    y_val =  df.index.tolist()
    graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_one = dict(title = 'Number of positive cases <br> per day',
                xaxis = dict(title = 'Number of cases',
                autotick=True),
                yaxis = dict(title = 'Date'),
                )

    # second chart plot 
    graph_two = []
    graph_two.append(
      go.Bar(
      x = df.Cumulative_number_of_positive_cases.tolist(),
      y = df.index.tolist(),
      name = country
      )
    )

    layout_two = dict(title = 'Cumulative number of positive cases <br> per day',
                xaxis = dict(title = 'Cumulative number of cases',),
                yaxis = dict(title = 'Date'),
                )


    # third chart plot
    graph_three = []
    x_val = df.Number_of_deaths.tolist()
    y_val =  df.index.tolist()
    graph_three.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_three = dict(title = 'Number of deaths <br> per day)',
                xaxis = dict(title = 'Number of deaths',
                autotick=True),
                yaxis = dict(title = 'Date'),
                )
    
    # fourth chart
    graph_four = []
    
    x_val = df.Cumulative_number_of_deaths.tolist()
    y_val = df.index.tolist()

    graph_four.append(
          go.Bar(
          x = x_val,
          y = y_val,
          name = country
          )
      )

    layout_four = dict(title = 'Cumulative number of deaths <br> per day',
                xaxis = dict(title = 'Cumulative number of deaths'),
                yaxis = dict(title = 'Date'),
                )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    
    
    return figures


# In[216]:


if __name__=='__main__':
    
    dataset =get_dataset()
    df = filter_data(dataset, country_name = 'Afghanistan', date = [dataset.index.min(), dataset.index.max()])

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

