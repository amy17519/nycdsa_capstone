# David Richard Steinmetz
# davidsteinmetz@gmail.com

# Supervisor function which calls functions to:
# 1. Get the recommendations from the graphlab model
# 2. Extract the cluster data from the graphlab model recommendations
# 3. Get data about businesses on the map from Yelp API
# 4. Classify the businesses using KNN to clusters based on the pre-run K-means model
# 5. Sort the businesses by cluster and rating to be able to rec good restaurants
# 6. Generate a list of recommended restaurants based on knowledge of model recs

from Cluster import *
import numpy as np


def supervisor(user_id, bounding_box, search_params):
    # --- Test structures
    test_biz_cluster = pd.Series(np.random.randint(1, 25, 20))
    test_model_recs = pd.DataFrame({'cluster': np.random.randint(1, 25, 10)})

    # --- Collaborative filtering recommendations (1 + 2)
    # gl_model = load_model('graphlab_model.pkl')               # Load graphlab model
    # model_recs = gl_model.predict(user_id)                    # Get model recommendations
    model_recs = test_model_recs                                # Get model recommendations
    model_clusters = get_model_clusters(model_recs)             # Get clusters for model recs

    # --- Classify and sort (3 + 4 + 5)
    biz = get_businesses_on_map(bounding_box, search_params)    # Get businesses on map
    # biz['cluster'] = get_map_clusters(biz)                    # Classify biz on map to clusters (KNN)
    biz['cluster'] = test_biz_cluster                           # Classify biz on map to clusters (KNN)
    sorted_biz = cluster_rating_sort(biz)                       # Sort biz by cluster and rating

    # --- Generate recommendations in new locale (6)
    map_recs = gen_map_recs(sorted_biz, model_clusters)         # Generate recs from biz on map

    return map_recs
