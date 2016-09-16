import FitGraphLab as FG

recommender = FG.GraphLabRecommmender()
# recommender object

recommender.LoadModel(train='full',type='ranking',modelName='ranking')
#the model loaded from /Users/Shared/yelp_data/ranking

recommendation = recommender.Recommend(modelType='ranking',user_ids=X,k=40)
# X is the numpy array of user_id, k is the number of items to recommend

