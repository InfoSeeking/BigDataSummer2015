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
        	
		
			
		

						
	
