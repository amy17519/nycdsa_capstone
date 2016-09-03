import pandas as pd
from ParseJSON import *


# Switch to directory of file you wish to import
dir_path = './01_External/01_Yelp/'

# Import data
bus = ParseJSON(fileName=dir_path+'yelp_academic_dataset_business.json')
chk = ParseJSON(fileName=dir_path+'yelp_academic_dataset_checkin.json')
rev = ParseJSON(fileName=dir_path+'yelp_academic_dataset_review.json')
tip = ParseJSON(fileName=dir_path+'yelp_academic_dataset_tip.json')
usr = ParseJSON(fileName=dir_path+'yelp_academic_dataset_user.json')

# Check to see the import worked
bus = pd.DataFrame(bus)
bus.head()
bus.describe()

States = ProcessID(bus, 'state')
States[0:5]

Hours = ProcessID(bus, 'hours')

attr = ProcessID(bus, 'attributes')
amb = ProcessID(attr, 'Ambience')
caters = ProcessID(attr, 'Caters')


amb = ProcessIDDavid(attr, 'Ambience')
