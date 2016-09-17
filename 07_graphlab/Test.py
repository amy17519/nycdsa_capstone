import FitGraphLab as FG

recommender = FG.GraphLabRecommmender()
# recommender object

recommender.LoadRestaurantTypeNMap(typeFile='diningOptions.csv',mapFile='restaurants_types.csv')

recommender.LoadModel(train='full',type='ranking',modelName='ranking')
#the model loaded from /Users/Shared/yelp_data/ranking

recommendation = recommender.Recommend(modelType='ranking',user_ids=X,k=40)
# X is the numpy array of user_id, k is the number of items to recommend

# The following calls recommend with user-chosen restaurant types

recommendation = recommender.Recommend(modelType='ranking',user_ids=X,k=40,business_types=['Chinese','American (New)','Others']) #the list

recommendation = recommender.Recommend(modelType='ranking',user_ids=X,k=40,business_types='Chinese') #allow 'Chinese' not within the list   

