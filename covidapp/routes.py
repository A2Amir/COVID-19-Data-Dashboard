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

    default_county  = ['United_States_of_America']

    dataset = get_dataset()
    map_data = set_map_data(dataset)
    five_top_countries, country_codes = get_the_top(map_data)


    five_top_countries = [country for country, code in five_top_countries]
    dates=[dataset.index.min(), dataset.index.max()]
    # the five top countries filter
    five_top_df = filter_data(dataset, country_name = five_top_countries, date = dates  )
    figures = return_figures(map_data, five_top_df)



        #figures.append(figure.items())
        # Parse the POST request countries list
    if (request.method == 'POST') and request.form :
         # the user selected country
        filter_df = filter_data(dataset, country_name = list(request.form.values()), date = dates  )
        user_selected_figure= return_figures(map_data, filter_df)
        default_county = list(request.form.values())

    else:
        filter_df = filter_data(dataset, country_name = default_county, date = dates  )
        user_selected_figure= return_figures(map_data, filter_df)

    for figure in user_selected_figure:
        figures.append(figure)




    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i,_ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON,
                           all_countries=country_codes,
                           default_county=default_county)
