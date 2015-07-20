import sys
import util
import tagger


reload(sys)  
sys.setdefaultencoding('utf8')


def remove_repetition(tweets):
	tweets=[tweet.lstrip("rt:\t") for tweet in tweets]
	tweets=list(set(tweets))
	return tweets

def if_not_topic(tweets,topic) :
	tweets=[tweet for tweet in tweets if topic in tweet ]
	return tweets	

def make_lowercase(tweets):
	tweets=[tweet.lower() for tweet in tweets]
	return tweets

def remove_newline(tweets) :
	tweets=[tweet.replace("\n"," ") for tweet in tweets]
	return tweets	

def only_char(line):
	tokens=line.split()
	words=[token for token in tokens if token.isalpha() and not token.lower()=="rt"]
	if len(words)==0 :
		return True
	else :
		return False 

def splitURL(pos_tweet):
	tweet , url , info ="" , "" , ""
	for token in pos_tweet :
		if token[1]=="U"  :
			url=url+" "+token[0]
		else :
			tweet=tweet+" "+token[0]
	y=[tweet.strip(" ") , url.strip(" ") ]
	return y

def common_except_url(pos_tweets):
	tweets=[ splitURL(pos_tweet) for pos_tweet in pos_tweets]
	url, texts , urls , ntweets=[] , [] ,[] ,[] 
	for tweet in tweets :
		if tweet[0] in texts :
			i=texts.index(tweet[0])
			urls[i]=urls[i]+" "+tweet[1]
		else :
			texts.append(tweet[0])
			urls.append(tweet[1])			
	for i in range(0,len(texts)) :
		if not texts[i]=="" and not texts[i]==" " and not only_char(texts[i]) :
			url=urls[i].split()
			if len(url)==0 :
				url=[""]
			ntweets.append(str(texts[i])+" "+str(url[0]))
	ntweets = [ ' '.join(tweet.split(" ")) for tweet in ntweets ]
	return ntweets			

def process(inPath,outPath,topics) :
	for topic in topics :
		inFile=inPath+'/'+topic+".csv" 
		tweets=util.csvTolist(inFile)
		tweets= [ str(tweet).strip("[']") for tweet in tweets ]
	
		print("No. of Tweets extracted "+str(topic)+"\t\t\t"+str(len(tweets)))
		tweets=make_lowercase(tweets)
		tweets=remove_repetition(tweets)
		tweets=remove_newline(tweets)
		tweets=if_not_topic(tweets,topic.lower())

		#POS-Tagging of tweets
		pos_tweets=tagger.runtagger_parse(tweets) #[[[tw1_token1,postag,confidence],[tw1_token2,postag,confidence]],[[tw2_token1,postag,confidence]]]
		tweets=common_except_url(pos_tweets)
		pos_tweets=tagger.runtagger_parse(tweets)
		
		print("No. of Tweets after cleaning :"+str(topic)+"\t\t\t"+str(len(tweets)))
		
		outFile=outPath+'/data_'+topic+".txt" 
		util.listTotxt(outFile,tweets,"w+") 
		outFile=outPath+'/POS_'+topic+".csv" 
		util.listTocsv(outFile,pos_tweets,"w+") 

