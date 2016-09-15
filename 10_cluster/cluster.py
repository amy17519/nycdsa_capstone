# David Richard Steinmetz
# Gregory Domingo
# NYCDSA Capstone Project

# import sys
from GetYelpData import search_yelp

# Get command line arguments
# total = len(sys.argv)
# args = str(sys.argv)


# Load clusters created from Yelp challenge dataset


# Load json file
def load_json(file_name):
    import io
    import json
    with io.open(file_name) as f:
        loaded = json.load(f)
    return loaded


# Yelp API call based on map GPS bounding box
def get_businesses_on_map():
    # Specify parameter files
    secret_file = 'yelp_secret.json'
    map_bounding_box_file = 'map_bounding_box.json'
    param_file = 'yelp_search_params.json'

    # Load bounding box and search params
    # Yelp secret data is loaded in search_yelp()
    gps = load_json(map_bounding_box_file)
    params = load_json(param_file)

    # Search and return data from Yelp API
    resp = search_yelp(secret_file, gps, params)
    return resp

# Assign restaurants on map to a cluster
