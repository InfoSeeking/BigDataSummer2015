#Script to extract tweets on different topics using Tweepy library for Python. 
#For more details, read http://tweepy.readthedocs.org/en/v3.2.0/getting_started.html#introduction
#The extracted tweets are saved to .csv file named according to topic name.
#To obtain API Keys and secret tokens for authorization, create a twitter developer account on https://apps.twitter.com/
#There is a Rate limit restriction on extraction of tweets which limits the number of tweets to be extracted in 15-minute window using REST API.For more details, read https://dev.twitter.com/rest/public/rate-limiting. 
#I noticed Rate Limit Error occured after around 3k tweets had been extracted and hence I used time.sleep() to wait for 16 mins after every 2.5k tweets were extracted

import tweepy
import time
import csv

#Authorization Tokens
API_KEY=api_key
API_SECRET=api_sec
ACCESS_TOKEN=acc_tok
ACCESS_TOKEN_SECRET=acc_toksec

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth) #if using proxy based server,add an argument proxy="http://username:pswrd@host:port/"

#Topics on which tweets were extracted
topic=['Mozilla','Nobel prize','fifa','ipl','obama','Modi','thanksgiving','beyonce','beatles','Higgs boson' ]

for i in range(0,10) :
	fname=topic[i]+'.csv'
	for tweet in tweepy.Cursor(api.search, q=topic[i],lang='en').items(2500) : #to extract 2.5k tweets on that topic
		print tweet.text
		print " "
		
		dataStrip = [] #list to store tweet attributes
		dataStrip.append(tweet.text.encode('utf-8'))

		with open(fname, "ab") as fp :
	     		writeFile = csv.writer(fp)
      			writeFile.writerow(dataStrip)
		fp.close()
		print("Waiting for 15 mins : Rate Limit Restriction ") 
		time.sleep(60*16) # Rate Limit Restriction on tweets extracted 
        	
		
			
		

						
	
