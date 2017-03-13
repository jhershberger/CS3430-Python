##Justin Hershberger
##A01381222
##Python 2.7

import scipy as sp
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk.stem
import sklearn.datasets

#define the train groups
train_groups = ['rec.autos', 'rec.motorcycles']

#get the data set we want
train_data = sklearn.datasets.fetch_20newsgroups(subset='train', categories=train_groups)

english_stemmer = nltk.stem.SnowballStemmer('english')

#use the StemmedTfidfvectorizer class from lecture
class StemmedTfidfvectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc:(english_stemmer.stem(w) for w in analyzer(doc))

tfidf_vectorizer = StemmedTfidfvectorizer(min_df=1, stop_words='english')

train_data_feat_mat = tfidf_vectorizer.fit_transform(train_data.data)

km = KMeans(n_clusters=10, n_init=1, verbose=1, random_state=3)
clustered_data = km.fit(train_data_feat_mat)

def find_top_n_closest_posts(new_post, vectorizer, kmeans, n):
    new_post_vec = vectorizer.transform([new_post])

    #get the top cluster of the feature vector
    top_post_label = km.predict(new_post_vec)[0]

    #get the indices of the feature vector in the same cluster
    close_post_indices = (km.labels_ == top_post_label).nonzero()[0]

    similar_posts = []

    #compute the distance between the feature vector and the similar posts
    for i in close_post_indices:
        dist = sp.linalg.norm((new_post_vec - train_data_feat_mat[i]).toarray())
        similar_posts.append((dist, train_data.data[i]))

    #sort the matches by distance
    similar_posts = sorted(similar_posts, key=lambda posts: posts[0])

    #display the top n posts
    for j in range(0,n):
        print "Post ", j, ", distance=", similar_posts[j][0]
        print similar_posts[j][1]


find_top_n_closest_posts("is the brand high quality?", tfidf_vectorizer, km, 2)
