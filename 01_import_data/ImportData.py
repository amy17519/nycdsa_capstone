# Switch to directory of file you wish to import

import sys
import pandas as pd

# For David
dir_list = ['D:\\Projects\\DataScienceBootcamp\\25_Project5_Capstone\\02_Selfgen',
            'D:\\Projects\\DataScienceBootcamp\\25_Project5_Capstone\\02_Selfgen\\01_import_data',
            'D:\\Projects\\DataScienceBootcamp\\25_Project5_Capstone\\02_Selfgen\\02_flask_app']
sys.path.extend(dir_list)  # Add dirs to system path

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
