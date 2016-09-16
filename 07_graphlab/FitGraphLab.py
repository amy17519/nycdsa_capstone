import graphlab, os
import pandas as pd
import numpy  as np
from ParseJSON import ParseJSON
from ProcessID import ProcessID
from collections import defaultdict

class GraphLabRecommmender(object):

      def __init__(self,mode='recommend'):

          if mode not in ['recommend', 'training']: raise ValueError('Bad mode %s' %(mode))

          if mode == 'training':
              self.userDF,self.reviewDF,self.businessDF = ConstructUserBusinessReviewDF()
              self.userSF     = graphlab.SFrame(self.userDF)
              self.businessSF = graphlab.SFrame(self.businessDF)
              self.total_review_data = graphlab.SFrame(self.reviewDF) 
          self.model_performance = dict()
          self.full_model        = dict()
          self.trained_model     = dict()
         
          self.model_parameters  = dict()
          self.model_parameters['ranking']       = dict()
          self.model_parameters['factorization'] = dict()
          self.model_parameters['ranking']['num_factors'] = 10
          self.model_parameters['ranking']['regularization'] = 0.1 
          self.model_parameters['ranking']['linear_regularization'] = 0.1  
          self.model_parameters['ranking']['max_iterations'] = 50   
          self.model_parameters['ranking']['size_data_factorization'] = False  
          self.model_parameters['factorization']['num_factors'] = 50
          self.model_parameters['factorization']['regularization'] = 1
          self.model_parameters['factorization']['linear_regularization'] = 1
          self.model_parameters['factorization']['max_iterations'] = 100
          self.model_parameters['factorization']['size_data_factorization'] = True

          self.elite_business_id = None

      def ComputeEliteBusinessIDs(self):

          if self.elite_business_id is not None: return
          self.elite_business_id = self.businessDF.loc[self.businessDF['elite_year']>0,['business_id']]


      def BuildTrainTestSamples(self):

          samples = np.array(np.random.randint(0,2,size=self.userDF.shape[0]),dtype=bool)
          self.trainDF = self.reviewDF.loc[samples,:]
          self.testDF  = self.reviewDF.loc[~samples,:]
          self.train_data = graphlab.SFrame(self.trainDF)
          self.test_data  = graphlab.SFrame(self.testDF)
          

      def TrainFactorizationModel(self,train='train'):

          params      = self.model_parameters['factorization']
          num_factors = params['num_factors']
          lambda_2    = params['regularization']
          lambda_1    = params['linear_regularization']
          max_iterations = params['max_iterations']
          size_data_factorization = params['size_data_factorization']
          train_data = self.train_data if train=='train' else self.total_review_data
          item_fac_model = graphlab.factorization_recommender.create(train_data, user_id='user_id', item_id='business_id', \
                      user_data=self.userSF,item_data=self.businessSF,target='stars',num_factors=num_factors,\
                      regularization=lambda_2,linear_regularization=lambda_1, max_iterations=max_iterations,\
                      size_data_factorization=size_data_factorization)

          if train=='train':
                 self.trained_model['factorization'] = item_fac_model 
          elif train=='full':
                 self.full_model['factorization']    = item_fac_model
          else:  raise ValueError("Bad train token")


      def TrainRankingModel(self,train='train'):

          params      = self.model_parameters['ranking']
          num_factors = params['num_factors']
          lambda_2    = params['regularization']
          lambda_1    = params['linear_regularization']
          max_iterations = params['max_iterations']
          size_data_factorization = params['size_data_factorization']
          train_data  = self.train_data if train=='train' else self.total_review_data
          item_rank_model = graphlab.ranking_factorization_recommender.create(train_data, user_id='user_id', item_id='business_id',\
                     user_data=self.userSF,item_data=self.businessSF,num_factors=num_factors,regularization=lambda_2,\
                     linear_regularization=lambda_1, side_data_factorization=False,max_iterations=max_iterations)

          if train=='train':
                 self.trained_model['ranking'] = item_rank_model
          elif train=='full':
                 self.full_model['ranking']    = item_rank_model
          else: raise ValueError("Bad train token")


      
      def TestModelPrecision(self,modelType='ranking'):

          if modelType=='ranking': 
               self.model_performance['ranking']       = graphlab.compare(self.test_data, [self.item_rank_model])
          elif modelType=='factorization': 
               self.model_performance['factorization'] = graphlab.compare(self.test_data, [self.item_fac_model])
          else:  raise ValueError("Invalid modelType " + modelType)

      def TrainFullModel(self,modelType):

          if modelType == 'factorization': self.TrainFactorizationModel(train='full')
          elif modelType == 'ranking':     self.TrainRankingModel(train='full')
          else: raise ValueError("bad modelType choice")


      def SaveRankingModel(self,train, modelName):
          
          self.SaveModel(train, type='ranking',modelName=modelName)

      def SaveFactorizationModel(self,train,modelName):

          self.SaveModel(train, type='factorization', modelName=modelName)

      def SaveModel(self, train, type, modelName):

          cwd = os.getcwd()
          if train not in ['train','full']: raise ValueError("train is not valid")
          if modelName not in ['ranking','factorization']: raise ValueError("bad modelName")

          myModelName = cwd+"/"+modelName

          if (train,modelName)==('train','ranking'):
              self.trained_model['ranking'].save(myModelName)
          elif (train,modelName)==('train','factorization'):
              self.trained_model['factorization'].save(myModelName)
          elif (train,modelName)==('full','ranking'):
              self.full_model['ranking'].save(myModelName)
          elif (train,modelName)==('full','factorization'):
              self.full_model['factorization'].save(myModelName)
 
          print("The model %s has been saved to %s" %(modelName,myModelName))         
 

      def LoadModel(self,train,type,modelName,dir=None):
 
          myDir = os.getcwd() if dir is None else dir
          myModelName = myDir + "/" + modelName
          
          myModel = graphlab.load_model(myModelName)

          if train not in ['train','full']: raise ValueError("train is not valid")
          if modelName not in ['ranking','factorization']: raise ValueError("bad modelName")

          if (train,modelName)==('train','ranking'):
              self.trained_model['ranking'] = myModel
          elif (train,modelName)==('train','factorization'):
              self.trained_model['factorization'] = myModel
          elif (train,modelName)==('full','ranking'):
              self.full_model['ranking'] = myModel
          elif (train,modelName)==('full','factorization'):
              self.full_model['factorization'] = myModel

          print("the model loaded from %s" %(myModelName))

      def Recommend(self, modelType, user_ids, eliteSpecial=False, k=60, business_categories=None,location=None):
 
           myModel = self.full_model[modelType]
           users   = pd.DataFrame(user_ids)
           users.columns = ['user_id']

           if not eliteSpecial:
                  userSF  = graphlab.SFrame(users)
                  recommended  = myModel.recommend(userSF,k=k).to_dataframe()
           else:
                  X = users.merge(self.userDF.loc[:,['user_id','elite_year']], on = 'user_id',how='left')
                  non_elites = np.array(X.loc[X['elite_year']==0,'user_id'])
                  elites     = np.array(X.loc[X['elite_year']>0,'user_id'])
                  if non_elites.shape[0]>0:
                       recommended_common = myModel.recommend(non_elites,k=k).to_dataframe()
                  else: recommended_common = None
                  if elites.shape[0]>0:
                       self.ComputeEliteBusinessIDs()
                       recommended_elite  = myModel.recommend(elites,k=k,items=graphlab.SFrame(self.elite_business_id)).to_dataframe()
     
                  if recommended_common is not None: 
                                recommended = recommended_common
                                if recommended_elite is not None: recommended = recommended.append(recommended_elite)
                  else:  recommended = recommended_elite

           return(recommended)



##########################################

def ConstructUserBusinessReviewDF():
   
    businessDF,business_id = LoadBusiness()

    userDF,reviewDF = LoadUserNReview(business_id)

    userDF,reviewDF,businessDF = AppendEliteYears(userDF,reviewDF,businessDF)

    userDF,reviewDF,businessDF = AppendCityState(userDF,reviewDF,businessDF)

    return(userDF,reviewDF,businessDF)

def LoadBusiness():

    business   = ParseJSON('yelp_academic_dataset_business.json')
    categories = ProcessID(business, 'categories')

    businessDF = pd.DataFrame(business)

    isRestaurant = np.array([u'Restaurants' in t for t in categories])
    businessDF['IsRestaurant'] = isRestaurant   # add an IsRestaurant column

    businessDF2 = businessDF.loc[businessDF['IsRestaurant'],:]   #  filter the IsRestaurant column

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

    businessDF3 = businessDF3.ix[:,['business_id','categories','review_count','stars','city','state','checkin_Num']]

    return(businessDF3,business_id)


def LoadUserNReview(business_id):

    users  = ParseJSON('yelp_academic_dataset_user.json')

    reviewDF = pd.read_csv('review.csv',sep='\t')  # pre-processed review csv file
    reviewDF = reviewDF.loc[reviewDF['business_id'].isin(business_id),:] # the list business_id is defined below in the business section.
    reviewDF = reviewDF.loc[:,['user_id','business_id','stars']]
    # It includes only the business which categories include 'Restaurant'

    x2=reviewDF.groupby('user_id')
    z2=x2.mean()
    stars = z2.loc[:,['user_id','stars']]


    userDF  = pd.DataFrame(users)
    userDF2 = userDF.loc[:,['user_id','average_stars','review_count','useful']]
    userDF2['useful_ratio'] = userDF2['useful']/(userDF2['review_count']+2.0)

    # compute the ratio of 'useful' to review count

    userDF3=userDF2.merge(stars,on='user_id',how='left')

    # left join the average stars from the restaurant type evaluation

    userDF3.ix[np.isnan(userDF3['stars']),'stars'] = userDF3.loc[np.isnan(userDF3['stars']),'average_stars']
    userDF3=userDF3.drop('average_stars',axis=1)

    # drop the average stars provided by yelp

    elites = ProcessID(users,'elite')
    elites = [list(map(lambda z:str(z),t)) for t in elites]

    userDF3=userDF3.loc[:,['user_id','review_count','stars']]

    userDF3['elites'] = np.array(elites)
    userDF3['elite_year'] = np.array([len(t) for t in elites])

    return(userDF3,reviewDF)


def AppendEliteYears(userDF, reviewDF, businessDF):


    x = userDF.loc[:,['user_id', 'elite_year']]
    y = reviewDF.loc[:,['user_id','business_id']]
    y = y.merge(x, on='user_id', how='left')
    z = y.groupby('business_id').sum()
    z['business_id'] = z.index
    businessDF = businessDF.merge(z,on='business_id',how='left')
    businessDF.loc[np.isnan(businessDF['elite_year']),'elite_year'] = 0

    return(userDF,reviewDF,businessDF)
    

def AppendCityState(userDF, reviewDF, businessDF):

    x = businessDF.loc[:,['business_id','city','state']]
    y = reviewDF.merge(x,on='business_id',how='left')
    y = y.loc[:,['user_id','city','state']]
    y.sort_values('user_id',inplace=True) 
    user_ids = y['user_id']
    city  = y['city']
    state = y['state']
    myCities = defaultdict(list)
    myStates = defaultdict(list)

    for idx, user in enumerate(user_ids):
 
        myCities[user].append(city[idx])
        myStates[user].append(state[idx])

    for user in list(set(userDF['user_id'])-set(user_ids)):

        myCities[user].extend([])
        myStates[user].extend([])

    X = pd.DataFrame(myCities.keys())
    X.columns = ['user_id']
    X['city'] = map(lambda x: list(set(x)),list(myCities.values()))
    X['state']= map(lambda x: list(set(x)),list(myStates.values()))
    userDF    = userDF.merge(X,on='user_id',how='left')
    
    return(userDF,reviewDF,businessDF)          
