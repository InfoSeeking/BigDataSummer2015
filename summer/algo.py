from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score,silhouette_score
import numpy as np
import util
import decimal as dec
import sys
import os

reload(sys)  
sys.setdefaultencoding('utf-8')

def get_max(data) :
	max=-99999999
	for i in range(0,len(data)):
		if data[i][1]>max :
			max=data[i][1]
	return max


def bm25(doc,topic,avgdl,datal):
	freq=doc.count(topic)
	tok=doc.split(" ")
	docl=len(tok)
	coeff=dec.Decimal(0.75*docl)/dec.Decimal(avgdl)
	num=freq*2.5
	den=dec.Decimal(freq+(1.5*(0.25+float(coeff))))
	val=dec.Decimal(num)/dec.Decimal(den)
	idf=dec.Decimal(0.5)/dec.Decimal(datal+0.5)
	result=idf*val
	return result

def rank_by_val(data,topic,ind):
	s=""
	for line in data :
		s=s+line+" "
	token=s.split(" ")
	avgdl=len(token)

	score , score1 , score2 , TopIndex=[] , [] ,[],[]
	for i in range(0,len(data)) :
		x=[ i , bm25(data[i],topic,avgdl,len(data)) ]
		score1.append(x)
		x[1]=len(str(data[i]))
		score2.append(x)
	max1=get_max(score1)
	max2=get_max(score2)
	
	for i in range(0,len(data)) :
		score1[i][1]=dec.Decimal(score1[i][1])/dec.Decimal(max1)
		score2[i][1]=dec.Decimal(score2[i][1])/dec.Decimal(max2)
		x=[ i , dec.Decimal(score1[i][1]+score2[i][1]) ]
		score.append(x)
	score=sorted(score,key=lambda x: dec.Decimal(x[1]),reverse=True)
	if ind<len(score) :
		score=score[0:ind]
	TopIndex=[ token[0] for token in score]
	return TopIndex

def ranker(rfile,data,topic,ind) :
	TopIndex=rank_by_val(data,topic,ind)
	TopData=[ data[j].encode("utf-8") for j in TopIndex ]
	util.listTotxt(rfile,TopData,"w+")
	return TopData

def Clustering(outfile,tweets,n_clusters,topic,k) :
	np.random.seed(0)
	vectorizer = TfidfVectorizer(stop_words='english')
	X = vectorizer.fit_transform(tweets)
	model = KMeans(n_clusters, init='k-means++', max_iter=500, n_init=20)
	model.fit(X)
	
	#Check for empty clusters if any
	Tweetclusters=list(model.predict(X))
	nonempty=[ i for i in range(0,n_clusters) if not Tweetclusters.count(i)==0 ]
	empty=list(set(range(0,n_clusters))-set(nonempty)) 
	print("Empty Clusters :"+str(topic)+" TOP "+str(k)+" KMEANS "+str(n_clusters)+" "+str(empty))

	#Write Tweetwise Clusters to File
	outfile1=os.path.dirname(outfile)+"/TWEET_CLUSTER_"+str(topic)+"_TOP_"+str(k)+"_KMEANS_"+str(n_clusters)+".txt"
	util.listTotxt(outfile1,Tweetclusters,"w+")
	
	#Get top ranked tweets from cluster 
	ind=int(k)/int(n_clusters)
	TopTweet ,ClusterAllIndex ,AllTopTweet = [] , [] , []
	for i in range(n_clusters) :
		ClusterTweets , ClusterIndex , TopClusterTweet=[] , [] ,[]
		for j in range(0,len(Tweetclusters)):
			if Tweetclusters[j]==i :
				ClusterTweets.append(tweets[j])
				ClusterIndex.append(j)
		ClusterAllIndex.append(ClusterIndex)
		TopClusterTweet=rank_by_val(ClusterTweets,topic,ind)
		TopTweet.append(TopClusterTweet)
		AllTopTweet.extend(TopClusterTweet)
	outfile1=os.path.dirname(outfile)+"/INDEX_"+str(topic)+"_TOP_"+str(k)+"_KMEANS_"+str(n_clusters)+".txt"
	util.listTotxt(outfile1,ClusterAllIndex,"w+")
	
	with open (outfile,"w+") as f:
		for i in range(len(AllTopTweet)) :
			j=AllTopTweet[i]
			f.write(str(tweets[j]).encode("utf-8")+"\n")

	outfile1=os.path.dirname(outfile)+"/CLUSTER_TWEETS_"+str(topic)+"_TOP_"+str(k)+"_KMEANS_"+str(n_clusters)+".txt"
	util.listTocsv(outfile1,TopTweet,"w+")
	
			
def intersect(tokens,allAspects) :
	x=[ token for token in tokens if token in allAspects ]
	return x

def GreedyNormal(outfile,TweetTokens,aspects,tweets,limit):
	TopInd , ctr =[] , []
	left=[aspect for aspect in aspects]
	
	for i in range(0,len(TweetTokens)) :	
		x=[ intersect(TweetTokens[i],left) , i ] 
		x.append(len(x[0]))
		ctr.append(x)

	ctr=sorted(ctr,key=lambda x: int(x[2]),reverse=True)
	while len(left)>0 and len(TopInd)<limit :
		TweetAsp=ctr[0][0] #aspects for that tweet
		TopInd.append(ctr[0][1])#index for tweet selected
		left=[ token for token in left if token not in TweetAsp ]
	        # remove aspect from other tweets aspects too as it is covered
		ctr.remove(ctr[0])
		for i in range(0,len(ctr)) :	
			ctr[i][0]=intersect(ctr[i][0], left) 
			ctr[i][2]=len(ctr[i][0])					
		ctr=sorted(ctr,key=lambda x: int(x[2]),reverse=True)

	results=[ tweets[i] for i in TopInd ]
	util.listTotxt( outfile, results , "w+")	
	return results
	
