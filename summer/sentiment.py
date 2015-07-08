#For sentiment classification of tweets using method described in 'Aspect-Based Twitter Sentiment Classification' by Hui Lek et al. 

import util
import math

TERMINATE=-5 
NEGATION_WINDOW=6

def found_negation(aspect,pos_tweet,wsize=NEGATION_WINDOW): 
	is_neg=False	
	if len(pos_tweet)<wsize :
		wsize=len(pos_tweet)
	ind=util.get_index(pos_tweet,aspect,0)
	if ind<wsize :
		start=0
		end=wsize-1
	else :
		start=wsize-ind+1
		end=ind	
	for i in range(start,end+1):
		word=pos_tweet[i][0]
		if util.is_in_file('lists/negative-words.txt',word,False) or util.is_in_file('lists/swear-words.txt',word,False):
			is_neg=True
	return is_neg		
	
		
def switch(polarity):
	if polarity=='+' :
		return '-'
	elif polarity=='-' :
		return '+'
	else :
		return '0'


def get_polarity(word,is_neg):
	if util.is_in_file('lists/positive-words.txt',word,False):
		polarity='+'
	elif util.is_in_file('lists/negative-words.txt',word,False):
		polarity='-'
	elif util.is_in_file('lists/swear-words.txt',word,False):
		polarity='-'
	else :
		polarity='0' 
	if is_neg :
		polarity=switch(polarity)
	return polarity

		
def left_verb_sentiment(aspect,pos_tweet,is_neg) :
	sentiment=['NULL']*3
	sentiment[0]=aspect	
	ctr=util.get_index(pos_tweet,aspect,0)-1
	while(pos_tweet[ctr][1]!='V' and ctr>=0)	:
		ctr=ctr-1
	else :
		if(pos_tweet[ctr][1]=='V' and ctr>=0) :
			verb=pos_tweet[ctr][0]
			sentiment[1]=verb
			sentiment[2]=get_polarity(verb,is_neg)
			ctr=TERMINATE
	return sentiment

def left_adverb_sentiment(aspect,pos_tweet,is_neg) :
	sentiment=['NULL']*3
	sentiment[0]=aspect	
	ctr=util.get_index(pos_tweet,aspect,0)-1
	while(pos_tweet[ctr][1]!='R' and ctr>=0)	:
		ctr=ctr-1
	else :
		if(pos_tweet[ctr][1]=='R' and ctr>=0) :
			adverb=pos_tweet[ctr][0]
			sentiment[1]=adverb
			if util.is_in_file('lists/comparative-words.txt',adverb,False) or util.is_in_file('lists/superlative-words.txt',adverb,False) :
				sentiment[2]=switch(get_polarity(adverb,is_neg))
			else :
				sentiment[2]=get_polarity(adverb,is_neg)
			ctr=TERMINATE
	return sentiment


def left_adjective_sentiment(aspect,pos_tweet,is_neg) :
	sentiment=['NULL']*3
	sentiment[0]=aspect	
	ctr=util.get_index(pos_tweet,aspect,0)-1
	while(pos_tweet[ctr][1]!='A' and ctr>=0)	:
		ctr=ctr-1
	else :
		if(pos_tweet[ctr][1]=='A' and ctr>=0) :
			adj=pos_tweet[ctr][0]
			sentiment[1]=adj
			if util.is_in_file('lists/comparative-words.txt',adj,False) or util.is_in_file('lists/superlative-words.txt',adj,False) : 
				sentiment[2]=switch(get_polarity(adj,is_neg))
			else :
				sentiment[2]=get_polarity(adj,is_neg)
			ctr=TERMINATE			
	return sentiment

def left_hashtag_sentiment(aspect,pos_tweet,is_neg) :
	sentiment=['NULL']*3
	sentiment[0]=aspect	
	ctr=util.get_index(pos_tweet,aspect,0)-1
	while(pos_tweet[ctr][1]!='#' and ctr>=0)	:
		ctr=ctr-1
	else :
		if(pos_tweet[ctr][1]=='#' and ctr>=0) :
			hashtag=pos_tweet[ctr][0]
			sentiment[1]=hashtag
			sentiment[2]=get_polarity(hashtag.lstrip('#'),is_neg)
			ctr=TERMINATE
	return sentiment

def right_verb_sentiment(aspect,pos_tweet,is_neg) :
	sentiment=['NULL']*3
	sentiment[0]=aspect	
	ctr=util.get_index(pos_tweet,aspect,0)+1
	while(ctr>=0 and ctr<len(pos_tweet) and pos_tweet[ctr][1]!='V')	:
		ctr=ctr+1
	else :
		if(ctr>=0 and ctr<len(pos_tweet) and pos_tweet[ctr][1]=='R') :
			verb=pos_tweet[ctr][0]
			sentiment[1]=verb
			if not(util.is_in_file('lists/copulative.txt',verb,False)) and not(util.is_in_file('lists/intensifier.txt',verb,False)) :
				sentiment[2]=get_polarity(verb,is_neg)
			else :
				sentiment[2]=str('0')
			ctr=TERMINATE
		return sentiment

def right_adverb_sentiment(aspect,pos_tweet,is_neg) :
	sentiment=['NULL']*3
	sentiment[0]=aspect	
	ctr=util.get_index(pos_tweet,aspect,0)+1
	while(ctr>=0 and ctr<len(pos_tweet) and pos_tweet[ctr][1]!='R')	:
		ctr=ctr+1
	else :
		if(ctr>=0 and ctr<len(pos_tweet) and pos_tweet[ctr][1]=='R') :
			adverb=pos_tweet[ctr][0]
			sentiment[1]=adverb
			if not(util.is_in_file('lists/intensifier.txt',adverb,False)) :
				if util.is_in_file('lists/comparative-words.txt',adverb,False) or util.is_in_file('lists/superlative-words.txt',adverb,False) :
					sentiment[2]=switch(get_polarity(adverb,is_neg))
				else :
					sentiment[2]=get_polarity(adverb,is_neg)
			ctr=TERMINATE
	return sentiment

def right_adjective_sentiment(aspect,pos_tweet,is_neg) :
	sentiment=['NULL']*3
	sentiment[0]=aspect	
	ctr=util.get_index(pos_tweet,aspect,0)+1
	while(ctr>=0 and ctr<len(pos_tweet) and pos_tweet[ctr][1]!='A')	:
		ctr=ctr+1
	else :
		if(ctr>=0 and ctr<len(pos_tweet) and pos_tweet[ctr][1]=='A') :
			adj=pos_tweet[ctr][0]
			sentiment[1]=adj
			if not(util.is_in_file('lists/intensifier.txt',adj,False)) :
				if util.is_in_file('lists/comparative-words.txt',adj,False) or util.is_in_file('lists/superlative-words.txt',adj,False) :
					sentiment[2]=switch(get_polarity(adj,is_neg))
				else :
					sentiment[2]=get_polarity(adj,is_neg)
			ctr=TERMINATE
	return sentiment

def right_hashtag_sentiment(aspect,pos_tweet,is_neg) :
	sentiment=['NULL']*3
	sentiment[0]=aspect	
	ctr=util.get_index(pos_tweet,aspect,0)+1
	while(ctr>=0 and ctr<len(pos_tweet) and pos_tweet[ctr][1]!='#')	:
		ctr=ctr+1
	else :
		if(ctr>=0 and ctr<len(pos_tweet) and pos_tweet[ctr][1]=='#') :
			hashtag=pos_tweet[ctr][0]
			sentiment[1]=hashtag
			sentiment[2]=get_polarity(hashtag.lstrip('#'),is_neg)
			ctr=TERMINATE		
	return sentiment



def get_sentiment(aspect,pos_tweet):
	sentiments=[]	
	nsentiments=[]
	is_neg=False
	if found_negation(aspect,pos_tweet) :
		is_neg=True
	sentiments.append(left_verb_sentiment(aspect,pos_tweet,is_neg))
	sentiments.append(left_adverb_sentiment(aspect,pos_tweet,is_neg))
	sentiments.append(left_adjective_sentiment(aspect,pos_tweet,is_neg))
	sentiments.append(left_hashtag_sentiment(aspect,pos_tweet,is_neg))
	sentiments.append(right_verb_sentiment(aspect,pos_tweet,is_neg))
	sentiments.append(right_adverb_sentiment(aspect,pos_tweet,is_neg))
	sentiments.append(right_adjective_sentiment(aspect,pos_tweet,is_neg))
	sentiments.append(right_hashtag_sentiment(aspect,pos_tweet,is_neg))
	nsentiments=[sentiment for sentiment in sentiments if sentiment[1]!='NULL' ]
	return nsentiments	

def classify_sentiment(sentiments):
	pctr=0
	nctr=0
	for i in range(0,len(sentiments)) :
		for j in range(0,len(sentiments[i])) :
			if sentiments[i][j][2]=="+" :
				pctr=pctr+1
			elif sentiments[i][j][2]=="-" :
				nctr=nctr+1
	print("PCTR : "+str(pctr)+" NCTR : "+str(nctr))
	if pctr>nctr :
		return "+"
	elif nctr>pctr :
		return "-"
	else:
		return "0"



def aspect_sentiment(aspects,pos_tweets) :
	nsentiments=[]	
	sentiments=[]
	aspect_senti=[]
	for i in range(0,len(aspects)) :
		for j in range(0,len(pos_tweets)) :
			if util.get_index(pos_tweets[j],aspects[i][0],0)!=-1 :
				sentiments.append(get_sentiment(aspects[i][0],pos_tweets[j]))
		nsentiments=[sentiment for sentiment in sentiments if sentiment!=[] ]
		polarity=classify_sentiment(nsentiments)
		x=["NULL"]*2
		x[0]=aspects[i][0]
		x[1]=polarity
		aspect_senti.append(x)
	return aspect_senti
