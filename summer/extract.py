#Script to extract tweets on different topics using Tweepy library for Python. 
#Topics are extracted from a .txt file containing topics which is provided as an arguement
#For eg :python extract.py topics.txt where topics.txt contains list of topics(each on a new line)
#To obtain API Keys and secret tokens for authorization, create a twitter developer account on https://apps.twitter.com/
#The extracted tweets are saved to data/raw_data/X.csv file where X is the topic name.
#There is a Rate limit restriction on extraction of tweets which limits the number of tweets to be extracted in 15-minute window using REST API.For more details, read https://dev.twitter.com/rest/public/rate-limiting. 
#I noticed Rate Limit Error occured after around 3k tweets had been extracted and hence I used time.sleep() to wait for 16 mins after every 2.5k tweets were extracted

import tweepy
import time
import sys
import os
import util


#Create a twitter developer a/c to get the API keys,tokens
<<<<<<< HEAD
API_KEY='cUTgURkmvAKPjar4NxE7qWh4v'
API_SECRET='VTUGm126JAr12uJdwpjkVWAlwoezt4cmzS0CADg1FTvmmMjIXe'
ACCESS_TOKEN='3222410820-Y3UBodT0cFvkKPebEcQEjgghMeAWzIDb8Kmo4Il'
ACCESS_TOKEN_SECRET='b4pjhTzx3dHcomEs5laNbpeMXH6pluhUsi04RxLAgrxfY'
=======
API_KEY=api_key
API_SECRET=api_secret
ACCESS_TOKEN=access_token
ACCESS_TOKEN_SECRET=access_token_secret
auth=tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth,proxy="http://u.padalkar:13908117@202.141.80.20:3128/") #if using proxy based server,add an argument proxy="http://username:pswrd@host:port/"
>>>>>>> 637f8ffac7dcaec5eb8efd1eb352669914ed2685


def getTweets(topic,PATH_TO_RAW_DATA,MAX_TWEETS) :
	auth=tweepy.OAuthHandler(API_KEY, API_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth,proxy="http://u.padalkar:13908117@202.141.80.20:3128/") #if using proxy based server,add an argument proxy="http://username:pswrd@host:port/"
	
	for topic in topics :
		print topic
		outFile=PATH_TO_RAW_DATA+'/'+topic+".txt" 
		ctr=0
		while ctr < MAX_TWEETS :
			data=tweepy.Cursor(api.search, q=topic,lang='en').items(500)
			try:
				tweets = [data.text.lower().encode('utf-8') for tweet in data ]
				ctr=ctr+len(tweets)
				util.listTotxt(outFile,tweets,"a+")
				
			except tweepy.error.TweepError :	
				print("Waiting for 15 mins : Rate Limit Restriction "+str(ctr)+" Tweets Extracted\n") 
				time.sleep(60*15) # Rate Limit Restriction on no. of tweets extracted in one 15-min window


