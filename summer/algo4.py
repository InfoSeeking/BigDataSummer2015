from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import adjusted_rand_score,silhouette_score
import pandas as pd
import os
from sklearn.decomposition import PCA
from sklearn import cluster
from scipy.spatial import distance
import sklearn.datasets
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np

def compute_bic(kmeans,X):
	centers = [kmeans.cluster_centers_]
	labels  = kmeans.labels_
	m = kmeans.n_clusters
	# size of the clusters
	n = np.bincount(labels)
	#size of data set
	N, d = X.shape

	#compute variance for all clusters beforehand
	distance.cdist(ref_1d[numpy.newaxis, :], query_2d)
	cl_var = (1.0 / (N - m) / d) * sum([sum(distance.cdist([np.where(labels == i)], [centers[0][i]], 'euclidean')**2) for i in range(m)])
	const_term = 0.5 * m * np.log(N) * (d+1)
	
	BIC=np.sum([n[i] * np.log(n[i]) -
               n[i] * np.log(N) -
             ((n[i] * d) / 2) * np.log(2*np.pi*cl_var) -
             ((n[i] - 1) * d/ 2) for i in range(m)]) - const_term

	return(BIC)

def k(data):
	np.random.seed(123)
	ks = [2,25,50,100]
	vectorizer = TfidfVectorizer(stop_words='english')
	X = vectorizer.fit_transform(data)
	n_clusters=50
	model = cluster.KMeans(n_clusters=50, init='k-means++', max_iter=500, n_init=20)
	print model.fit(X)
	
	#plt.plot(X[:,0],X[:,1])
	#plt.show()


