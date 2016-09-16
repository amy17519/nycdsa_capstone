from ProcessID import ProcessID
import FitGraphLab as FG
import pandas as pd

recommender = FG.GraphLabRecommmender()
# recommender object

recommender.LoadModel(train='full',type='ranking',modelName='ranking')
#the model loaded from /Users/Shared/yelp_data/ranking

X = pd.DataFrame({'user_id': ['8J4IIYcqBlFch8T90N923A',
                              'QXwSbE7fwXlBROW6E_FcqQ']})

recommendation = recommender.Recommend(modelType='ranking',user_ids=X,k=40)
# X is the numpy array of user_id, k is the number of items to recommend

