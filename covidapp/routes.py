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


    countries_selected = [country for country, code in country_default]
    dates=[dataset.index.min(), dataset.index.max()]
    # the five top countries filter
    filter_df = filter_data(dataset, country_name = countries_selected, date = dates  )
    figures = return_figures(map_data, filter_df)

    # the user selected country
    filter_df = filter_data(dataset, country_name = ['Iran'], date = dates  )
    user_selected_figure= return_figures(map_data, filter_df)
    for figure in user_selected_figure:
        figures.append(figure)


    #figures.append(figure.items())
    # Parse the POST request countries list
    if (request.method == 'POST') and request.form:
        print(request.form)
		#figures = return_figures(request.form)




    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i,_ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON,
                           all_countries=country_codes,
                           countries_selected=countries_selected)
