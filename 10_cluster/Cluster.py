# David Richard Steinmetz - davidsteinmetz@gmail.com
# Gregory Domingo
# NYCDSA Capstone Project

# import sys
import os
import pandas as pd
os.chdir('C:\\Users\\root\\Projects\\DataScienceBootcamp\\25_Project5_Capstone\\02_Selfgen\\06_yelp_api')
# os.chdir('./02_Selfgen/06_yelp_api')
from GetYelpData import search_yelp
os.chdir('C:\\Users\\root\\Projects\\DataScienceBootcamp\\25_Project5_Capstone\\02_Selfgen\\10_cluster')
# os.chdir('../10_cluster')


# Load json file
def load_json(file_name):
    import io
    import json
    with io.open(file_name) as f:
        loaded = json.load(f)
    return loaded


# Yelp API call based on map GPS bounding box
def get_businesses_on_map(bounding_box, search_params):
    # Specify parameter files
    secret_file = 'yelp_secret.json'
    # map_bounding_box_file = 'map_bounding_box.json'
    # param_file = 'yelp_search_params.json'

    # Load bounding box and search params
    # Yelp secret data is loaded in search_yelp()
    # gps = load_json(map_bounding_box_file)
    # params = load_json(param_file)

    # Search and return data from Yelp API
    # resp = search_yelp(secret_file, gps, params)
    resp = search_yelp(secret_file, bounding_box, search_params)

    # ADD SECTION TO FORMAT DATA FOR KNN PREDICT
    business_data = [
        {
            'name': business.name,
            'id': business.id,
            'url': business.url,
            'rating': business.rating,
            'top_category': business.categories[0].alias if business.categories else '',
            'display_phone': business.display_phone,
            'display_address': business.location.display_address,
            'latitude': business.location.coordinate.latitude,
            'longitude': business.location.coordinate.longitude
        }
        for business in resp.businesses
        ]

    return pd.DataFrame(business_data)


# Load clusters created from Yelp challenge dataset
# http://stackoverflow.com/questions/10592605/save-classifier-to-disk-in-scikit-learn
def load_pickle(file_name):
    import cPickle
    with open(file_name, 'r') as fid:
        return cPickle.load(fid)


# Assign restaurants on map to a cluster
def get_map_clusters(business_data):
    # from sklearn import KNeighborsClassifier  # do we need this?
    knn = load_pickle('knn_model.pkl')
    return knn.predict(business_data)


# Sort businesses by cluster and rating
def cluster_rating_sort(business_data):
    return business_data.sort_values(['cluster', 'rating'], ascending=[True, False])


# Extract clusters from top model recommendations
def get_model_clusters(model_recs, num_clust):
    unique = model_recs['cluster'].drop_duplicates()
    if len(unique) >= num_clust:
        clusters = unique[0:num_clust]
    else:
        clusters = unique[0:len(unique)]
    return clusters


# Return map recommendations per cluster (location tuple, business attr)
def gen_map_recs(sdata, clusters):
    filter_by = sdata['cluster'].isin(clusters)     # T/F dataframe to filter by clusters
    reduced = sdata[filter_by]                      # filter dataset
    return reduced.groupby('cluster').head(2)       # extract first two business per cluster
    # return sdata


# CREATE PREDICT FUNCTION FOR DBS
def dbscan_predict(centroids, new_resto):
    import numpy as np

    data = new_resto.values
    ans = np.arange(data.shape[0])
    X = centroids.values
    for i in range(data.shape[0]):
        dist = np.sum((X - data[i, :].reshape(1, -1)) ** 2, axis=1)
        cluster_id = np.argmin(dist)
        ans[i] = cluster_id
    return (ans)

### MAKE TEST RECORD FOR PREDICT DBS CLUSTER (no predict function for dbs)
# new_resto = gl.SFrame({'stars': [4.5, 5, 4],
#                   'PriceRange': [1,1,1],
#                   'LogReviewCnt': [1.38629436,2.9957322,3.04452243772]})
# dbscan_predict(Centroids,new_resto.to_dataframe())
