import os

def gl_model(user_id, num_rec):
    import FitGraphLab as FG

    recommender = FG.GraphLabRecommmender()
    # recommender object

    recommender.LoadRestaurantTypeNMap(typeFile='diningOptions.csv',
                                       mapFile='restaurants_types.csv',
                                       typeDir='./')

    recommender.LoadModel(train='full', type='ranking', modelName='ranking')
    # the model loaded from ./ranking/

    # recommendation = recommender.Recommend(modelType='ranking',
    #                                        user_ids=user_id,
    #                                        k=num_rec)

    recommendation = recommender.Recommend(modelType='ranking',
                                           user_ids=user_id,
                                           k=40,
                                           business_types=['Chinese', 'American (New)', 'Others'])  # the list

    # user_id is the numpy array of user_id, k is the number of items to recommend

    return recommendation

