import pandas as pd
import matplotlib.pyplot as plt


# ProcessID imported from ParseJSON.py

# Business data --------------------------------------------------------
# bus imported in ImportData.py
buspd = pd.DataFrame(bus, index=range(len(bus)))
bus[0].keys()

# Extract city, state and full address
city = ProcessID(bus, 'city')
state = ProcessID(bus, 'state')
fulladd = ProcessID(bus, 'full_address')
revcnt = ProcessID(bus, 'review_count')


# CITY
len(set(city))  # 412 unique cities
pd.Series(city).value_counts()[0:20]  # Las Vegas has most reviews at 17423


# STATE
len(set(state))
pd.Series(state).value_counts()
# Not in the US
buspd[buspd.state == 'QC'][['latitude', 'longitude']]  # Quebec, Canada
buspd[buspd.state == 'EDH'][['latitude', 'longitude']]  # Edinburgh, Scotland
buspd[buspd.state == 'BW'][['latitude', 'longitude']]  # Baden-Württemburg, Germany
buspd[buspd.state == 'ON'][['latitude', 'longitude']]  # Ontario, Canada
buspd[buspd.state == 'MLN'][['latitude', 'longitude']]  # Midlothian, Scotland
buspd[buspd.state == 'RP'][['latitude', 'longitude']]  # Rheinland-Pfalz, Germany
buspd[buspd.state == 'ELN'][['latitude', 'longitude']]  # Edinburgh, Scotland
buspd[buspd.state == 'FIF'][['latitude', 'longitude']]  # Edinburgh, Scotland
buspd[buspd.state == 'SCB'][['latitude', 'longitude']]  # Edinburgh, Scotland
buspd[buspd.state == 'KHL'][['latitude', 'longitude']]  # Edinburgh, Scotland
buspd[buspd.state == 'NW'][['latitude', 'longitude']]  # Baden-Württemberg, Germany
buspd[buspd.state == 'HAM'][['latitude', 'longitude']]  # Edinburgh, Scotland
buspd[buspd.state == 'NTH'][['latitude', 'longitude']]  # Edinburgh, Scotland

out_of_us = ['QC', 'EDH', 'BW', 'ON', 'MLN', 'RP', 'ELN', 'FIF', 'SCB', 'KHL', 'NW', 'HAM', 'NTH']
in_us = list(set([state for state in buspd.state if state not in out_of_us]))
buspd['in_us'] = buspd['state'].isin(in_us)
grp = buspd.groupby('in_us')
grp.size()/len(buspd)*100  # 87% in US, 13% out of US


# REVIEW COUNT
grp.agg('mean')['review_count']  # Mean review count is significantly higher for businesses in the US (~34 vs. ~14)
buspd['review_count'].value_counts()[0:10]
plt.hist(buspd['review_count'].value_counts(), bins=100)
#


# Checkin data --------------------------------------------------------

# Review data ---------------------------------------------------------
# rev imported in ImportData.py
rev[0].keys()
rev[0]['text']

# Tip data ------------------------------------------------------------


# User data --------------------------------------------------------