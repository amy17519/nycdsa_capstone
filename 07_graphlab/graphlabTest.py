import graphlab, pd
import numpy  as np
from ParseJSON import ParseJSON, ProcessID

users  = ParseJSON('yelp_academic_dataset_user.json')

reviewDF = pd.read_csv('review.csv',sep='\t')  # pre-processed review csv file
reviewDF = reviewDF.loc[reviewDF['business_id'].isin(business_id),:] # the list business_id is defined below in the business section.
# It includes only the business which categories include 'Restaurant'

x2=reviewDF.groupby(['user_id'])
z2=x2.mean()
stars = z2.loc[:,['user_id','stars']]

userDF2=userDF.loc[:,['user_id','average_stars','review_count','useful']]
userDF2['useful_ratio'] = userDF2['useful']/(userDF2['review_count']+2.0)

# compute the ratio of 'useful' to review count

userDF3=userDF2.merge(stars,on='user_id',how='left')

# left join the average stars from the restaurant type evaluation

userDF3.ix[np.isnan(userDF3['stars']),'stars'] = userDF3.loc[np.isnan(userDF3['stars']),'average_stars']
userDF3=userDF3.drop('average_stars')

# drop the average stars provided by yelp

elites = ProcessID(users,'elite')

elites = [list(map(lambda z:str(z),t)) for t in elites]

userDF3=userDF3.loc[:,['user_id','review_count','useful_ratio','stars']]

userDF3['elites'] = np.array(elites)
userDF3['elite_year'] = np.array([len(t) for t in elites])

# add the elite status years and the number of such years into the data frame

userSF = graphlab.SFrame(userDF3)   # convert to SFrame

userSF.print_rows(num_rows=10)      

#+------------------------+--------------+----------------+---------------+------------+
#|        user_id         | review_count |  useful_ratio  |     stars     | elite_year |
#+------------------------+--------------+----------------+---------------+------------+
#| 18kPq7GPye-YQ3LyKyAZPw |     108      | 2.54545454545  |      4.14     |     2      |
#| rpOyqD_893cqmDAtJLbdog |     1274     | 11.1277429467  | 3.77777777778 |     11     |
#| 4U9kSBLuBDU391x6bxU-YA |     442      | 3.34009009009  |      4.0      |     11     |
#| fHtTaujcyKvXglE33Z5yIw |      11      | 0.846153846154 |      4.64     |     0      |
#| SIBCL7HBkrP4llolm4SC2A |      66      |      0.5       |      3.8      |     1      |
#| 8J4IIYcqBlFch8T90N923A |     1611     | 10.9764414135  |      4.35     |     11     |
#| ysYmC-ufbdmVEX9yAv-VEQ |      55      | 0.684210526316 |      4.45     |     3      |
#| WPOKvkacSKHx_bIG1alFiA |      60      | 2.11290322581  |      3.88     |     1      |
#| UTS9XcT14H2ZscRIf0MYHQ |     101      | 2.35922330097  | 3.36363636364 |     0      |
#| qL7Astun3i7qwr2IL5iowA |      20      | 1.36363636364  |      4.3      |     0      |
#+------------------------+--------------+----------------+---------------+------------+
#+-------------------------------+
#|             elites            |
#+-------------------------------+
#|          [2005, 2006]         |
#| [2005, 2006, 2007, 2008, 2... |
#| [2005, 2006, 2007, 2008, 2... |
#|               []              |
#|             [2005]            |
#| [2005, 2006, 2007, 2008, 2... |
#|       [2005, 2006, 2007]      |
#|             [2005]            |
#|               []              |
#|               []              |
#+-------------------------------+
#[552339 rows x 6 columns]

business   = ParseJSON('yelp_academic_dataset_business.json')
categories = ProcessID(business, 'categories')

businessDF = pd.DataFrame(business)

isRestaurant = np.array([u'Restaurants' in t for t in categories])
businessDF['IsRestaurant'] = isRestaurant   # add an IsRestaurant column

businessDF2 = businessDF.loc[businessDF['IsRestaurant'],:]     filter the IsRestaurant column

business_id = list(set(businessDF2['business_id']))  # find the unique business ID from restaurant related business

checkins  = ParseJSON('yelp_academic_dataset_checkin.json')

x = pd.DataFrame()
x['business_id'] = ProcessID(checkins,'business_id')
checkin_info     = ProcessID(checkins,'checkin_info')
checkin_Num      = [len(t.keys()) for t in checkin_info]
x['checkin_Num'] = checkin_Num

businessDF3 = businessDF2.merge(x,on='business_id',how='left')

# add the number of check ins to the business attributes

businessDF3.loc[np.isnan(businessDF3['checkin_Num']),'checkin_Num']=0

# add number of check-ins to business attribute

businessDF3 = businessDF3.ix[:,['business_id','categories','review_count','stars','state','checkin_Num']]

businessSF = graphlab.SFrame(businessDF3)
businessSF.print_rows(num_rows=10)

#+------------------------+-------------------------------+--------------+-------+
#|      business_id       |           categories          | review_count | stars |
#+------------------------+-------------------------------+--------------+-------+
#| 5UmKMjUEUNdYWqANhGckJw |    [Fast Food, Restaurants]   |      4       |  4.5  |
#| mVHrayjG3uZ_RLHkLj-AMg | [Bars, American (New), Nig... |      20      |  5.0  |
#| KayYbHCt-RkbGcPdGOThNg | [Bars, American (Tradition... |      21      |  4.0  |
#| wJr6kSA5dchdgOdwH6dZ2w | [Burgers, Breakfast & Brun... |      8       |  3.5  |
#| fNGIbpazjTRdXgwRY_NIXA | [Bars, American (Tradition... |      7       |  4.0  |
#| b9WZJp5L1RZr4F1nxclOoQ | [Breakfast & Brunch, Sandw... |      58      |  4.5  |
#| zaXDakTd3RXyOa7sMrUE1g |      [Cafes, Restaurants]     |      6       |  3.5  |
#| WETE_LykpcnrC1sFcQ5EGg | [Pubs, Irish, Nightlife, B... |      7       |  3.0  |
#| rv7CY8G_XibTx82YhuqQRw |         [Restaurants]         |      5       |  3.5  |
#| SQ0j7bgSTazkVQlF5AnqyQ |     [Chinese, Restaurants]    |      9       |  2.5  |
#+------------------------+-------------------------------+--------------+-------+
#+-------+-------------+
#| state | checkin_Num |
#+-------+-------------+
#|   PA  |     0.0     |
#|   PA  |     16.0    |
#|   PA  |     41.0    |
#|   PA  |     12.0    |
#|   PA  |     10.0    |
#|   PA  |     44.0    |
#|   PA  |     13.0    |
#|   PA  |     7.0     |
#|   PA  |     0.0     |
#|   PA  |     5.0     |
#+-------+-------------+
#[25071 rows x 6 columns]


item_fac_model = graphlab.factorization_recommender.create(train_data, user_id='user_id', item_id='business_id', user_data=userSF,item_data=businessSF,target='stars',num_factors=20,regularization=0.1,linear_regularization=0.1, max_iterations=25)

model_performance = graphlab.compare(test_data, [item_fac_model])


# surprsingly, Another model which performs similarly but easier to train (shorter time)

item_fac_model = graphlab.ranking_factorization_recommender.create(train_data, user_id='user_id', item_id='business_id', user_data=userSF,item_data=businessSF,num_factors=50,regularization=0.1,linear_regularization=0.1,side_data_factorization=False)
