# Switch to directory of file you wish to import

import pandas as pd
from ParseJSON import *

cd './01_External/01_Yelp/'
bus = ParseJSON(fileName='yelp_academic_dataset_business.json')
chk = ParseJSON(fileName='yelp_academic_dataset_checkin.json')
rev = ParseJSON(fileName='yelp_academic_dataset_review.json')
tip = ParseJSON(fileName='yelp_academic_dataset_tip.json')
usr = ParseJSON(fileName='yelp_academic_dataset_user.json')
cd '../../'

# Check to see the import worked
bus = pd.DataFrame(bus)
bus.head()
bus.describe()

States = ProcessID(bus, 'state')
States[0]