import os

def gl_model(user_id, num_rec):
    import FitGraphLab as FG

    recommender = FG.GraphLabRecommmender()
    # recommender object

    recommender.LoadModel(train='full', type='ranking', modelName='ranking',dir="./scripts")
    # the model loaded from ./ranking/

    recommendation = recommender.Recommend(modelType='ranking',
                                           user_ids=user_id,
                                           k=num_rec)
    # user_id is the numpy array of user_id, k is the number of items to recommend

    return recommendation
