#To mine aspects from tweets -DONE
# To create a tweet-sentiment-aspect tuple -ONGOING 

import tagger 
import sys
import csv

def writePostweets(fname,pos_tweets):
	with open(fname,'a') as f:	
		wr = csv.writer(f)
		wr.writerows(pos_tweets)
	f.close()

def parse_but(pos_tweets) :
	for pos_tweet in pos_tweets :
		for pos_token in pos_tweet :
			if pos_token[0]=="but" :
				pos_tweet=pos_tweet[pos_tweet.index(pos_token)+1:]
	return pos_tweets

def get_aspect(pos_tweets) :
	aspects=[]
	for pos_tweet in pos_tweets :
		aspect=[]
		for pos_token in pos_tweet :
			if pos_token[1]=='^' or pos_token[1]=='@' :
				aspect.append(str(pos_token[0]))
		if len(aspect)==0 :
			aspect.append('-')
		aspects.append(aspect)
	return aspects
			
reload(sys)  
sys.setdefaultencoding('utf8')
file_name = sys.argv[1]
pos_tweets=tagger.runtagger_parse(file_name)
writePostweets('TaggedModi.csv',pos_tweets)
pos_tweets=parse_but(pos_tweets)
aspects=get_aspect(pos_tweets)
print aspects
print pos_tweets[0][3][0]
print("Done")
