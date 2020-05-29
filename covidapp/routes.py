from covidapp import app
from flask import render_template
from wrangling_scripts.wrangle_data import get_dataset
from wrangling_scripts.wrangle_data import filter_data
from wrangling_scripts.wrangle_data import return_figures

import json, plotly

@app.route('/')
@app.route('/index')
def index():

    dataset = get_dataset()
    dates=[dataset.index.min(), dataset.index.max()]
    filter_df = filter_data(dataset, country_name = 'United_States_of_America', date =dates)
    figures= return_figures(dataset,filter_df)
    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i,_ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON)
