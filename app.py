from flask import Flask, request, render_template, jsonify
import lightkurve as lk
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import requests
import json
import numpy as np

app = Flask(__name__)

def calculate_number_of_trees(habitability, amplitude):
    # Convert habitability and amplitude to dimensionless scalars
    habitability = habitability.value if hasattr(habitability, 'value') else habitability
    amplitude = amplitude.value if hasattr(amplitude, 'value') else amplitude

    # Calculate the number of trees based on habitability score and amplitude
    num_trees = int(habitability * 10) + int(amplitude * 100)

    # Normalize the number of trees between 0 and 500
    # tree_normalized = min(500, num_trees / 1000 * 500)
    tree_normalized = num_trees/10000

    return num_trees, tree_normalized

def determine_habitability(num_trees, amplitude):
    # Convert num_trees and amplitude to dimensionless scalars
    num_trees = num_trees.value if hasattr(num_trees, 'value') else num_trees
    amplitude = amplitude.value if hasattr(amplitude, 'value') else amplitude

    # Calculate habitability as a combination of the number of trees and amplitude
    habitability = (num_trees * 0.1) + (amplitude * 0.01)
    return habitability

def determine_life_type(habitability):
    # Determine the most likely type of life based on habitability score
    if habitability >= 80:
        return "Advanced life forms such as animals and plants"
    elif habitability >= 60:
        return "Complex life forms such as fungi and multicellular organisms"
    elif habitability >= 40:
        return "Microbial life such as bacteria and archaea"
    else:
        return "No known life forms"

def determine_resource_type(habitability):
    # Determine the resource type based on star and planet radius
    # if star_radius > 1.0 and planet_radius > 1.0:
    #     return "Heavy elements such as gold, silver, and iron"
    # else:
    #     return "Basic resources such as carbon and minerals"
    if habitability >= 5000:
        return "Complex resources such as rare minerals and metals"
    else:
        return "Basic resources such as carbon and minerals" # Can we calculate this based on period & type of star?

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        tic_id = request.form['tic_id']

        try:
            lc = lk.search_lightcurve(tic_id).download()
            flux = lc.flux
            median_flux = np.nanmedian(flux)  # Calculate the median using numpy

            # Calculate the number of trees based on habitability and median flux
            num_trees, tree_normalized = calculate_number_of_trees(habitability=50, amplitude=median_flux)  # You can adjust the habitability value here

            # Determine habitability score
            habitability = determine_habitability(num_trees, median_flux)

            # Determine the most likely type of life
            life_type = determine_life_type(habitability)

            # Determine the resource type based on habitability
            resource_type = determine_resource_type(habitability)

            response_data = {
                'tic_id': tic_id,
                'amplitude': median_flux,
                'num_trees': tree_normalized,
                'habitability': habitability,
                'life_type': life_type,
                'resource_type': resource_type
            }

            return jsonify(response_data)  # Return the response data as JSON
            
        except Exception as e:
            error_message = str(e)
            return render_template('error.html', error_message=error_message)

    return render_template('index.html')

def determine_planet_type(star_radius, star_mass, period, median_flux):
    # Perform the planet type determination logic based on star information, period, and median flux
    # Adjust the conditions and thresholds as needed for your classification scheme
    if star_radius < 1.0 and star_mass < 1.0 and period < 10 and median_flux < 0.5:
        return "Rocky Planet"
    elif star_radius > 1.0 and star_mass > 1.0 and period > 100 and median_flux > 1.0:
        return "Gas Giant"
    else:
        return "Unknown"

if __name__ == '__main__':
    app.run()