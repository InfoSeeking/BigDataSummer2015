# Aspect Mining and Sentiment Classification from tweets
# Method described in 'Aspect-Based Twitter Sentiment Classification' by Hui Lek et al 
# Takes a .csv file containing tweets as an arguement : All tweets should be in first column
# for tweets format , example file in 'data/raw_data' folder (extracted using extract.py)
#Eg command : python main.py data/raw_data/X.csv
#Creates two files in data/tagged_data folder :
# 1. File containg POS-Tagged tweets : POS_X.csv where X.csv is file containing tweets(command line arguement)
# 2. File containg Aspect-Sentiment pair for tweets : Sentiment_X.csv where X.csv is file containing tweets(command line arguement)

import sys
import tagger
import util
import aspect
import sentiment 
import os
import ranking
import algo
from decimal import Decimal, getcontext
import error
import clean
import math
import measures
import algo2
import algo3


DIR_PATH_TAGGED="data/tagged_data"

# utf-8 encoding to include emoticons etc all kinds of spl chars found in tweets		
reload(sys)  
sys.setdefaultencoding('utf8')
"""
#python main.py /../X.csv
file_path=sys.argv[1]
file_name=os.path.basename(file_path)
file_name=file_name.strip("\n")
if not os.path.exists(DIR_PATH_TAGGED):
  	os.makedirs(DIR_PATH_TAGGED)

print("\nCleaning Data")
tweets=util.csvColTolist(file_path,0)
print("No. of Tweets extracted :"+str(len(tweets)))
tweets=clean.make_lowercase(tweets)
tweets=clean.remove_repetition(tweets)
tweets=clean.remove_newline(tweets)
topic=file_name.rstrip(".csv")
tweets=clean.if_not_topic(tweets,topic.lower())

print("POS-Tagging of tweets") 
pos_tweets=tagger.runtagger_parse(tweets) #[[[tw1_token1,postag,confidence],[tw1_token2,postag,confidence]],[[tw2_token1,postag,confidence]]]
ind=clean.if_only_url(pos_tweets)
tweets=util.remove_ind(tweets,ind)
pos_tweets=util.remove_ind(pos_tweets,ind)
tweets=clean.common_except_url(pos_tweets)
pos_tweets=tagger.runtagger_parse(tweets)

print("No. of Tweets extracted after cleaning :"+str(len(tweets)))
with open (DIR_PATH_TAGGED+'/data_'+topic+".txt","w+") as f:
	for i in range(len(tweets)) :
		f.write(str(tweets[i]))
		f.write("\n")

util.listTocsv(DIR_PATH_TAGGED+'/POS_'+file_name,pos_tweets)

print("\nExtracting Top-100 Tweets")


t=["HTC","Beyonce","Uber","Obama","Samsung"]
for i in range(0,len(t)) :
	tweets=util.txtTolist("data/tagged_data/data_"+t[i]+".txt")
	res=tweets[0:100]
	l=measures.entropy(tweets)
	print(" random Entropy all "+str(t[i])+" "+str(l))
	l=measures.entropy(res)
	print(" random Entropy 100 "+str(t[i])+" "+str(l))
	l=measures.levenshtein(res)
	print(" random Levenshtein Distance "+str(t[i])+" "+str(l))
"""

print("1. By Unsupervised Clustering : K-Means ")
t=["Samsung"]
for i in range(0,len(t)) :
	tweets=util.txtTolist("data/tagged_data/data_"+t[i]+".txt")
	print len(tweets)
	n=[50,100]
	for ni in range(0,len(n)) :
		algo2.k_means_clustering(tweets,n[ni],t[i])
		res=util.txtTolist("results/new/"+str(t[i])+"_"+"TOP100_k_means"+str(n[ni])+".txt")
		l=measures.entropy(res)
		print(" K-means "+str(t[i])+" "+str(n[ni])+" Entropy "+str(l))
		l=measures.levenshtein(res)
		print(" K-means "+str(t[i])+" "+str(n[ni])+" Levenshtein Distance "+str(l))
	


"""
	
print("2. By Ranking  ")
t=["HTC","Beyonce","Uber","Obama","Samsung"]
for i in range(0,len(t)) :
	tweets=util.txtTolist("data/tagged_data/data_"+t[i]+".txt")
	rtweets=algo2.ranker(tweets,t[i].lower(),100)
	with open ('results/new/TOP100_RANKING_'+str(t[i])+".txt","w+") as f:
		for i in range(len(rtweets)) :
			f.write(str(rtweets[i]).encode("utf-8"))
			f.write("\n")
	l=measures.entropy(rtweets)
	print(" RANKING Entropy "+str(l))
	l=measures.levenshtein(rtweets)
	print(" RANKING Levenshtein Distance "+str(l))


print("3.Aspect based")
t=["Obama"]
for i in range(0,len(t)) :
	res=util.txtTolist("results/GREEDY1_"+t[i]+".txt")
	l=measures.entropy(res)
	print(" ASPECT Entropy GREEDY 1 "+str(t[i])+" "+str(l))
	l=measures.levenshtein(res)
	print(" ASPECT Levenshtein Distance GREEDY 1 "+str(t[i])+" "+str(l))

print("3.Aspect based")
t=["Obama"]
for i in range(0,len(t)) :
	res=util.txtTolist("results/GREEDY3_"+t[i]+".txt")
	l=measures.entropy(res)
	print(" ASPECT Entropy GREEDY 3 "+str(t[i])+" "+str(l))
	l=measures.levenshtein(res)
	print(" ASPECT Levenshtein Distance GREEDY 3 "+str(t[i])+" "+str(l))



#print("3. By Topic Modelling : LDA ")
#algo3.do_lda(tweets,n_clusters)

print("4. By aspect mining from tweets")

aspects_tweet=aspect.get_aspect(pos_tweets) # tweetwise aspects [[asp1,asp2],[],[asp1]]
print("\naspect_Ranking_and_Selection")
aspect_freq=ranking.get_freq(aspects_tweet) 
aspect_freq=sorted(aspect_freq,key=lambda x: int(x[1]),reverse=True)
aspect_freq=error.correct(aspect_freq)
aspects_sel=util.filter_rlist(aspect_freq,10,1)


util.listTocsv('results/ASPECTS_'+file_name,aspects_sel)
aspects=util.listfromlist(aspects_sel,0)
print aspects
#aspect_hits=ranking.pmi_list(aspects,topic,"results/pmi_"+topic+".csv")
aspect_hits=util.csvTolist("results/pmi_"+topic+".csv")
print aspect_hits
aspect_hits=sorted(aspect_hits,key=lambda x: float(x[1]),reverse=True)
util.listTocsv('results/ASPECTS_SORTED_'+file_name,aspect_hits)
asp_hits=util.filter_rlist(aspect_hits,6,1)
print asp_hits
print len(asp_hits)
#asp_score=ranking.in_both(asp_hits,aspects_sel)
#asp_score=ranking.get_avg_rank(aspects_sel,aspect_hits)
#asp_score=sorted(asp_score,key=lambda x: int(x[1]),reverse=True)
#print asp_score
#util.listTocsv(DIR_PATH_TAGGED+'/Aspect3_'+file_name,asp_score)
#lim=math.floor((len(aspect_hits)+len(aspects_sel))/2)
#print lim 
#asp_score=util.filter_rlist(asp_score,lim,1)
#print len(asp_score)
#util.listTocsv(DIR_PATH_TAGGED+'/Aspect4_'+file_name,asp_score)
#sentiment classification of tweets
#aspect_senti=sentiment.aspect_sentiment(aspects_sel,pos_tweets) 
#util.listTocsv(DIR_PATH_TAGGED+'/Sentiment1_'+file_name,aspect_senti)
#maximum cover
aspects1=util.listfromlist(asp_hits,0)
t_ind=algo.greedy(aspects_tweet,aspects1,tweets,topic)
print("% of aspects covered")
cover=len(aspects1)-len(t_ind)
total=len(aspects1)
print cover
print total
getcontext().prec = 6
p=Decimal(cover)/Decimal(total)
print (p*100)

#BPGraph=algo.make_BPGraph(aspects_tweet,aspects)
#t_ind1=algo.maxBPM(BPGraph)
#print(len(t_ind1))
cover=algo.mincover(aspects_tweet,aspects1,tweets,topic)
t_ind2=len(cover)
print t_ind2
print("% of aspects covered")
cover=t_ind2
total=len(aspects1)
print cover
print total
getcontext().prec = 6
p=Decimal(cover)/Decimal(total)
print (p*100)


t_ind3=algo.greedy2(aspects_tweet,aspects1,tweets,topic)
print("% of aspects covered")
cover=len(aspects1)-len(t_ind3)
total=len(aspects1)
print cover
print total
getcontext().prec = 6
p=Decimal(cover)/Decimal(total)
print (p*100)

t_ind3=algo.greedy3(aspects_tweet,aspects1,tweets,topic)
print("% of aspects covered")
cover=len(aspects1)-len(t_ind3)
total=len(aspects1)
print cover
print total
getcontext().prec = 6
p=Decimal(cover)/Decimal(total)
print (p*100)


print("ASPECT MINING + SENTIMENT CLASSIFICATION : DONE")
"""
