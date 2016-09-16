# Use Latent Dirichlet Allocation (LDA) to group sets of reviews
# as an input for KNN on businesses
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
    from time import time
    print "Loading dataset..."
    t0 = time()
    rev = ParseJSON(fileName=file_name)
    txt = ProcessID(rev, 'text')
    del rev
    print "done in %0.3fs." % (time() - t0)
    return txt


def create_tf(doc_list, n_features):
    from time import time
    from sklearn.feature_extraction.text import CountVectorizer
    print "Creating term frequency vector..."
    t0 = time()
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                                    stop_words='english')
    term_freq = tf_vectorizer.fit_transform(doc_list)
    print "done in %0.3fs." % (time() - t0)
    return term_freq


def fit_lda_model(tf, n_features, n_topics):
    from time import time
    from sklearn.decomposition import LatentDirichletAllocation
    print("Fitting LDA models with tf features, n_features=%d..."
          % n_features)
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                    learning_method='online', learning_offset=50.,
                                    random_state=0)
    t0 = time()
    lda.fit(tf)
    print("done in %0.3fs." % (time() - t0))
    return lda


# Get topics derived from the LDA model
def get_lda_topics(lda, doc_list, n_top_words, n_features):
    from sklearn.feature_extraction.text import CountVectorizer
    print("\nTopics in the LDA model:")
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                                    stop_words='english')
    tf_vectorizer.fit_transform(doc_list)
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)


# Write a subset of the review text to a file to speed loading
def write_subset_to_txt(review_text, file_name, num_lines):
    with open(file_name, 'w') as f:
        import re
        to_write = [re.sub('[\n]', '', line) for line in review_text[0:num_lines]]
        for s in to_write:
            f.write((s + u'\n').encode('utf-8'))


# Load subset of review text from a txt file
def load_review_subset(file_name):
    with open(file_name, 'r') as f:
        my_list = [line.decode('utf-8').rstrip(u'\n') for line in f]
    return my_list


# Example use
n_features = 1000
n_topics = 10
n_top_words = 20

dir_path = './01_External/01_Yelp/'
# f = dir_path + 'yelp_academic_dataset_review.json'
# txt = load_reviews(f)
f2 = './02_Selfgen/06_yelp_api/yelp_reviews_subset.txt'
txt = load_review_subset(f2)

# Create and print model
tf = create_tf(txt, n_features=n_features)
lda = fit_lda_model(tf, n_features, n_topics)
get_lda_topics(lda, txt, n_top_words, n_features=n_features)

# More stuff to see model output
indx = np.random.choice(tf.shape[0], 1)[0]
text = txt[indx]
print text
print '-' * 88
print lda.transform(tf[indx, :])

topic_lst = [0, 6, -1]
from sklearn.feature_extraction.text import CountVectorizer
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                                stop_words='english')
tf_vectorizer.fit_transform(txt)
tf_feature_names = tf_vectorizer.get_feature_names()
for topic in topic_lst:
    print ' '.join([tf_feature_names[i] for i in lda.components_[topic].argsort()[:-n_top_words - 1:-1]])
    print '-' * 88
