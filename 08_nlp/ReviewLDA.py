# Use Latent Dirichlet Allocation (LDA) to group sets of reviews
# as an input for KNN on businesses
from time import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from ParseJSON import *
import numpy as np


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print


# Load dataset
def load_reviews(file_name):
    print "Loading dataset..."
    t0 = time()
    rev = ParseJSON(fileName=file_name)
    txt = ProcessID(rev, 'text')
    del rev
    print "done in %0.3fs." % (time() - t0)
    return txt


def create_tf(doc_list):
    print "Creating term frequency vector..."
    t0 = time()
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                                    stop_words='english')
    tf = tf_vectorizer.fit_transform(doc_list[0:10])
    print "done in %0.3fs." % (time() - t0)
    return tf


def fit_lda_model(tf, n_features, n_topics):
    print("Fitting LDA models with tf features, n_features=%d..."
          % n_features)
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                    learning_method='online', learning_offset=50.,
                                    random_state=0)
    t0 = time()
    lda.fit(tf)
    print("done in %0.3fs." % (time() - t0))
    return lda


def get_lda_topics(lda, n_top_words):
    print("\nTopics in LDA model:")
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                                    stop_words='english')
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)


n_features = 100
n_topics = 10
n_top_words = 20

dir_path = './01_External/01_Yelp/'
f = dir_path + 'yelp_academic_dataset_review.json'
txt = load_reviews(f)
test = create_tf(txt)


indx = np.random.choice(tf.shape[0], 1)[0]
text = data_samples[indx]

print text
print '-' * 88
print lda.transform(tf[indx, :])

topic_lst = [0, 6, -1]

for topic in topic_lst:
    print ' '.join([tf_feature_names[i] for i in lda.components_[topic].argsort()[:-n_top_words - 1:-1]])
    print '-' * 88
