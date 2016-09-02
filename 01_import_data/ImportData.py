# Switch to directory of file you wish to import

import pandas as pd
import ParseJSON

cd './01_External/01_Yelp/'
bus = ParseJSON.ParseJSON(fileName='yelp_academic_dataset_business.json')
chk = ParseJSON.ParseJSON(fileName='yelp_academic_dataset_checkin.json')
rev = ParseJSON.ParseJSON(fileName='yelp_academic_dataset_review.json')
tip = ParseJSON.ParseJSON(fileName='yelp_academic_dataset_tip.json')
usr = ParseJSON.ParseJSON(fileName='yelp_academic_dataset_user.json')
cd '../../'

# Check to see the import worked
bus = pd.DataFrame(bus)
bus.head()
bus.describe()
