# For aspect mining from tweets using method described in 'Aspect-Based Twitter Sentiment Classification' by Hui Lek et al. 

import util
import error
import ranking
import algo
import tagger

def parse_but(pos_tweets) :
	for pos_tweet in pos_tweets :
		for pos_token in pos_tweet :
			if pos_token[0]=="but" :
				pos_tweet=pos_tweet[pos_tweet.index(pos_token)+1:]
	return pos_tweets

def get_aspect(pos_tweets) :
	pos_tweets=parse_but(pos_tweets)
	aspects_list=[]
	for pos_tweet in pos_tweets :
		aspect_tweet=[]
		for pos_token in pos_tweet :
			if pos_token[1]=='^' or pos_token[1]=='@' or pos_token[1]=='Z' or pos_token[1]=='M' or pos_token[1]=='N':
				aspect_tweet.append(str(pos_token[0]))		
		aspects_list.append(aspect_tweet)
	return aspects_list

def GreedyAspectRanking(outfile,tweets,topic,k) :
		
	pos_tweets=tagger.runtagger_parse(tweets)
	aspects_tweet=get_aspect(pos_tweets) # tweetwise aspects [[asp1,asp2],[],[asp1]]
	"""
	aspect_freq=ranking.get_freq(aspects_tweet) 
	aspect_freq=sorted(aspect_freq,key=lambda x: int(x[1]),reverse=True)
	aspect_freq=error.correct(aspect_freq)
	aspects_sel=util.filter_rlist(aspect_freq,10,1)

	util.listTocsv(outfile1,aspects_sel)
	aspects=util.listfromlist(aspects_sel,0)
	#aspect_hits=ranking.pmi_list(aspects,topic,"results/pmi_"+topic+".csv")
	"""
	aspect_hits=util.csvTolist("results/pmi_"+topic+".csv")
	aspect_hits=sorted(aspect_hits,key=lambda x: float(x[1]),reverse=True)
	#util.listTocsv(outfile,aspect_hits)
	asp_hits=util.filter_rlist(aspect_hits,6,1)
	aspects1=util.listfromlist(asp_hits,0)

	results=algo.GreedyNormal(outfile,aspects_tweet,aspects1,tweets,k)
	return results

		
