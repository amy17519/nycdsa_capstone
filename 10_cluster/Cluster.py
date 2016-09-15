# David Richard Steinmetz
# Gregory Domingo
# NYCDSA Capstone Project

# import sys
from GetYelpData import search_yelp


# Get command line arguments
# total = len(sys.argv)
# args = str(sys.argv)


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

    # ADD SECTION TO FORMAT DATA FOR KNN PREDICT
    business_data = resp

    return business_data


# Load clusters created from Yelp challenge dataset
# http://stackoverflow.com/questions/10592605/save-classifier-to-disk-in-scikit-learn
def load_model(file_name):
    # from sklearn import KNeighborsClassifier  # do we need this?
    import cPickle
    with open(file_name, 'rb') as fid:
        return cPickle.load(fid)


# Assign restaurants on map to a cluster
def get_clusters(business_data):
    # from sklearn import KNeighborsClassifier  # do we need this?
    knn = load_model('knn_model.pkl')
    return knn.predict(business_data)


# Sort businesses by cluster and rating
def bus_sort(business_data):
    import pandas as pd
    business_data = pd.DataFrame(business_data)
    business_data['cluster'] = get_clusters(business_data)
    return business_data.sort_values(['cluster', 'rating'], ascending=[True, False])


# Extract clusters from top model recommendations


# Return map recommendations per cluster (location tuple, business attr)
