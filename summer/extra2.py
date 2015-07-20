
		
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




	

def complement(l,val) :
	x=[]
	for i in range(0,val):
		if i in l :
			continue
		else :
			x.append(i)
	return x

def aspf(l,ctr,allaspects):
	a=[]
	ind=[]
	for i in range(0,len(ctr)) :
		if ctr[i][1] in l :
			 a = list(set(a) | set(ctr[i][0]))
	for i in range(0,len(a)) :
		ind.append(allaspects.index(a[i]))
	ind=list(set(ind))
	return ind

def get_neighbours(r2,allaspects,ctr,l1) :
	t2=[]
	asp=[]
	t=[]
	for i in range(0,len(r2)):
		asp.append(allaspects[r2[i]])
	for i in range(0,len(ctr)) :
		for a in asp :
			if a in ctr[i][0] :
				t.append(ctr[i][1])
	t=list(set(t))
	for t1 in t :
		if t1 in l1 :
			continue
		else :
			t2.append(t1)
	return t2
	

def mincover(alltweetasp,allaspects,tweets,topic) :
	left=[asp for asp in allaspects]
	ctr=[]
	l1=[]
	l2=[]
	r1=[]
	r2=[]
	for i in range(0,len(alltweetasp)) :	
		x=["NULL"]*3
		x[0]=cleandata(alltweetasp[i],allaspects)
		x[1]=i 
		x[2]=len(x[0])
		ctr.append(x)
	ctr=sorted(ctr,key=lambda x: int(x[2]),reverse=True)
	n=[ctr[0][1]]
	while len(n)>=0 and len(l1)<=100 :
		print("len : "+str(len(l1)))
		l1 = list(set(l1) | set(n))
		l2=complement(l1,len(alltweetasp))
		r1=aspf(l1,ctr,allaspects)
		r2=complement(r1,len(allaspects))
		n=get_neighbours(r2,allaspects,ctr,l1)
	print("len : "+str(len(l1)))
	with open ("results/MINCOVER_"+topic+".txt","w+") as f:
		for i in range(len(l1)) :
			j=l1[i]
			f.write(str(tweets[j]).encode("utf-8"))
			f.write("\n")
	return r1
		
#matching for vertex u is possible
def bpm(bpGraph,u,seen,matchR):
#Try every job one by one
	N=len(seen)
    	for v in range(0,N) :
        # If tweet u is interested in aspect v and v is not covered
        	if bpGraph[u][v] and not seen[v] :
        		seen[v] = True #Mark v as visited
        #If aspect 'v' is not assigned to a tweet OR previously assigned tweet for aspect v (which is matchR[v]) has an alternate aspect available. 
         #Since v is marked as visited in the above line, matchR[v] in the following recursive call will not get aspect 'v' again
            		if (matchR[v] < 0 or bpm(bpGraph, matchR[v], seen, matchR)) :
            	 		matchR[v] = u
               	 		return True
        return False;
 
# Returns maximum number of matching from M to N
def maxBPM(bpGraph) : #bp[no.of tweets][aspects]
#An array to keep track of the tweets covering aspects. The value of matchR[i] is the tweets number
#assigned to aspect i, the value -1 indicates nobody is assigned.
	asize=len(bpGraph[0])
    	matchR=[-1]*asize
        ind=[]
    	for u in range(0,len(bpGraph)) :
        	#Mark all ASPECTS as not seen for next TWEET
        	seen=[0]*asize
        	# Find if the TWEET 'u' can COVER ASPECT
 	        if (bpm(bpGraph, u, seen, matchR)) :
 	 	       ind.append(u)			
	return ind

def make_BPGraph(aspects_tweet,aspects) :
	stweet=len(aspects_tweet)
	sasp=len(aspects)
	y=[0]*sasp
	x=[y]*stweet
	for i in range(0,stweet) :
		n=len(aspects_tweet[i])
		if n!=0 :
			for j in range(0,n) :
				if aspects_tweet[i][j] in aspects :				
					k=aspects.index(aspects_tweet[i][j])
					x[i][k]=1
	return x




def cover(ind,BPGraph) :
	asize=len(BPGraph[0])
    	cover=[-1]*asize
	for index in ind :
		for j in range(0,len(BPGraph[index])) :
			if BPGraph[index][j]==1 :
				cover[j]=1
	zeros=0
	for asp in cover :
		if asp!=1 :
			zeros=zeros+1
	cover.append(zeros)
	return cover



	







		print("ASPECT MINING + SENTIMENT CLASSIFICATION : DONE")
		

def greedy2(outfile,alltweetasp,allaspects,data,topic,limit):
	left=[asp for asp in allaspects]
	tweets=[]
	ctr=[]
	asp_sel=[]
	for i in range(0,len(allaspects)) :
		asp_ctr=[]
		asp_ctr.append(allaspects[i])
		asp_ctr.append(0)
		asp_sel.append(asp_ctr)
	for i in range(0,len(alltweetasp)) :	
		x=["NULL"]*3
		x[0]=cleandata(alltweetasp[i],allaspects)
		x[1]=i 
		x[2]=len(x[0])
		ctr.append(x)
	ctr=sorted(ctr,key=lambda x: int(x[2]),reverse=True)
	ear=len(ctr)
	ctr=util.filter_rlist(ctr,1,2)
	nex=len(ctr)
	di=ear-nex
	while len(left)!=0 and len(ctr)>0 and len(tweets)<limit:
		if select_tweet(asp_sel,ctr[0][0]) :
			aspects_tweet=ctr[0][0] #aspects for that tweet
			tweets.append(ctr[0][1])#index for tweet selected
			for i in range(0,len(aspects_tweet)) : # for each remaining aspect from tweet selected
				for tok in range(0,len(asp_sel)) :
					if asp_sel[tok][0].lower()==aspects_tweet[i].lower() : 
						asp_sel[tok][1]=asp_sel[tok][1]+1
				if aspects_tweet[i] in left :
					left.remove(aspects_tweet[i])  # remove that aspect from left
					for j in range(1,len(ctr)) :    # remove aspect from other tweets aspects too as it is covered
						if aspects_tweet[i] in ctr[j][0] :
							ctr[j][0].remove(aspects_tweet[i])	
							ctr[j][2]=len(ctr[j][0])
					
			ctr[0][0]=[]
			ctr[0][2]=len(ctr[0][0])
		else :
			tok=ctr[0]
			ctr.remove(tok)
		ctr=sorted(ctr,key=lambda x: int(x[2]),reverse=True)
	x=[]
	x.append(left)
	x.append(tweets)
	with open (outfile,"w+") as f:
		for i in range(len(tweets)) :
			j=tweets[i]
			f.write(str(data[j]).encode("utf-8"))
			f.write("\n")
	print("len tweets "+str(len(tweets)))
	percentw= len(left)*100
	percentw=percentw/len(allaspects)
	percentw=100-percentw
	print("% "+str(percentw))
	print("di "+str(di))	
	util.listTocsv("Aspectdiff_"+topic+"csv",asp_sel)
	return left		


def select_tweet(asp_sel,aspects) :
	sel=False
	for aspect in aspects :
		i=-1
		for tok in range(0,len(asp_sel)) :
			if asp_sel[tok][0].lower()==aspect.lower() : 
				sel=True
	return sel


def get_asp_score(asplist,allaspects) :
	size=len(allaspects)
	score=0
	for asp in asplist :
		i=size
		if asp in allaspects :
			i=allaspects.index(asp)
		score=score+size-i	
	return score

def greedy3(outfile,alltweetasp,allaspects,data,topic,limit):
	left=[asp for asp in allaspects]
	tweets=[]
	ctr=[]
	asp_sel=[]
	for i in range(0,len(allaspects)) :
		asp_ctr=[]
		asp_ctr.append(allaspects[i])
		asp_ctr.append(0)
		asp_sel.append(asp_ctr)
	for i in range(0,len(alltweetasp)) :	
		x=["NULL"]*3
		x[0]=cleandata(alltweetasp[i],allaspects)
		x[1]=i 
		x[2]=get_asp_score(x[0],allaspects)
		ctr.append(x)
	ctr=sorted(ctr,key=lambda x: int(x[2]),reverse=True)
	ear=len(ctr)
	ctr=util.filter_rlist(ctr,1,2)
	nex=len(ctr)
	di=ear-nex
	while len(left)!=0 and len(ctr)>0 and len(tweets)<limit:
		if select_tweet(asp_sel,ctr[0][0]) :
			aspects_tweet=ctr[0][0] #aspects for that tweet
			tweets.append(ctr[0][1])#index for tweet selected
			for i in range(0,len(aspects_tweet)) : # for each remaining aspect from tweet selected
				for tok in range(0,len(asp_sel)) :
					if asp_sel[tok][0].lower()==aspects_tweet[i].lower() : 
						asp_sel[tok][1]=asp_sel[tok][1]+1
				if aspects_tweet[i] in left :
					left.remove(aspects_tweet[i])  # remove that aspect from left
					for j in range(1,len(ctr)) :    # remove aspect from other tweets aspects too as it is covered
						if aspects_tweet[i] in ctr[j][0] :
							ctr[j][0].remove(aspects_tweet[i])	
							ctr[j][2]=get_asp_score(x[0],allaspects)
							
					
			ctr[0][0]=[]
			ctr[0][2]=0
		else :
			tok=ctr[0]
			ctr.remove(tok)
		ctr=sorted(ctr,key=lambda x: int(x[2]),reverse=True)
	x=[]
	x.append(left)
	x.append(tweets)
	with open (outfile,"w+") as f:
		for i in range(len(tweets)) :
			j=tweets[i]
			f.write(str(data[j]).encode("utf-8"))
			f.write("\n")
	return left	


