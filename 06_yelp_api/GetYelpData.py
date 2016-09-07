# Extract Yelp Data through the API

import io
import json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

# read API keys
with io.open('config_secret.json') as cred:  # Auth in file not shared on github
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

# There are three ways to query the Search API: search, search_by_bounding_box, and
# search_by_coordinates. For each of these methods, additional parameters are optional.
# The full list of parameters can be found on the Search API Documentation.
# https://github.com/Yelp/yelp-python
params = {
    'term': 'food',
    'lang': 'en'
}

# search_by_bounding_box takes a southwest latitude/longitude and a northeast
# latitude/longitude as the location boundary
sw_latitude, sw_longitude = 37.900000, -122.500000
ne_latitude, ne_longitude = 37.788022, -122.399797
response = client.search_by_bounding_box(
    sw_latitude,
    sw_longitude,
    ne_latitude,
    ne_longitude,
    **params
)


# Function to extract response locations
def get_response_coords(resp):
    coord = []

    for i in range(len(resp.businesses)):
        latitude = resp.businesses[i].location.coordinate.latitude
        longitude = resp.businesses[i].location.coordinate.longitude
        if latitude and longitude:
            coord.append((latitude, longitude))

    return coord

# Retrieve latitude and longitude from the response object
get_response_coords(response)

# Parse response documentation:
# https://www.yelp.com/developers/documentation/v2/search_api
# response.businesses[0].name
