from covidapp import app
from flask import render_template, request, Response, jsonify
from wrangling_scripts.wrangle_data import get_dataset
from wrangling_scripts.wrangle_data import filter_data
from wrangling_scripts.wrangle_data import return_figures
from wrangling_scripts.wrangle_data import set_map_data
from wrangling_scripts.wrangle_data import get_the_top


import json, plotly

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    dataset = get_dataset()
    map_data = set_map_data(dataset)
    country_default, country_codes = get_the_top(map_data)
    # Parse the POST request countries list

    countries_selected = [country for country, code in country_default]
    dates=[dataset.index.min(), dataset.index.max()]
    filter_df = filter_data(dataset, country_name = countries_selected, date = dates  )
    figures = return_figures(map_data, filter_df)


    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i,_ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON,
                           all_countries=country_codes,
                           countries_selected=countries_selected)
