# David Richard Steinmetz
# NYCDSA - Capstone Project


# Gets Yelp RSS feed; user credentials must be stored in
# a json file and supplied as an argument
def get_rss_feed(credentials_file):
    import mechanize
    import cookielib
    import re
    import json
    import io

    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    br.addheaders = [('User-agent', 'Chrome')]

    # The site we will navigate into, handling its session
    br.open('https://www.yelp.com/login')

    # View available forms
    # for f in br.forms():
    #     print f

    # Select the fifth (index four) form (the one to login)
    br.select_form(nr=4)

    # User credentials
    with io.open(credentials_file) as cred:
        creds = json.load(cred)
    br.form['email'] = creds['email']
    br.form['password'] = creds['password']

    # Login
    br.submit()

    # Get RSS feed
    rss_html = br.open('https://www.yelp.com/rss').read()
    rss_re = re.search('http://www\.yelp\.com/syndicate/user/(.{22})/rss\.xml', rss_html)
    if rss_re:
        rss_url = rss_re.group(0)  # URL is entire regex match, group 0
        user_id = rss_re.group(1)  # User ID is first matching regex group, group 1
        rss_feed = br.open(rss_url).read()
    else:
        raise ValueError('No RSS feed URL found; check Yelp login credentials')

    return rss_feed


# Parse XML
def parse_rss(feed):
    from bs4 import BeautifulSoup
    import re
    soup = BeautifulSoup(feed, 'lxml')
    reviews = soup.find_all('title')
    reviews.pop(0)  # Remove RSS feed title, keep review titles
    geo_lat = soup.find_all('geo:lat')
    geo_long = soup.find_all('geo:long')

    rev_val = []  # Initialize review values (stars) list
    rev_lat = []  # Initialize latitude list
    rev_long = []  # Initialize longitude list

    for i in range(len(reviews)):  # Extract review values
        stars = re.search('[(]([0-5])[/][5][)]', reviews[i].get_text()).group(1)
        if stars:
            rev_val.append(int(stars))
        else:
            rev_val.append([])

        lat = float(geo_lat[i].get_text())
        if lat:
            rev_lat.append(lat)
        else:
            rev_lat.append([])

        lng = float(geo_long[i].get_text())
        if lng:
            rev_long.append(lng)
        else:
            rev_long.append([])

    info = {'stars': rev_val,
            'longitude': rev_long,
            'latitude': rev_lat}

    return info


# Example use
rss = get_rss_feed('yelp_login.json')
review_info = parse_rss(rss)
review_info


# Example yelp_login.json
# {
#     "email": "davidsteinmetz@gmail.com",
#     "password": "my_password"
# }
