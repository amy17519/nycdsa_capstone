# Extract Yelp Data through the API

import io
import json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

# read API keys
with io.open('config_secret.json') as cred:
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
response = client.search_by_bounding_box(
    37.900000,
    -122.500000,
    37.788022,
    -122.399797,
    **params
)

# Parse response documentation:
# https://www.yelp.com/developers/documentation/v2/search_api
response.businesses[0].name
