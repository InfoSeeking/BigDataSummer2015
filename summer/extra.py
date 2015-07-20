def get_normlev_dist(word1,word2) :	
	dec.getcontext().prec = 10
	m=len(word1)
	n=len(word2) 
	x=[0]*n	
	d=[x]*m
	for i in range(0,m):
      		d[i][0]= i
        for j in range(0,n):
        	d[0][j]= j 
	for j in range(0,n) :
		for i in range(0,m) :
			if word1[i] == word2[j]:
				d[i][j] = d[i-1][j-1]             
			else:
				d[i][j] = min(d[i-1][j] + 1, d[i][j-1] + 1, d[i-1][j-1] + 1) 
	
	val= dec.Decimal(d[m-1][n-1])/dec.Decimal(m*n)
	return val

def levenshtein(data) : #Tweetwise Normalized Levenshtein Distance and Sum it over doc to get Levenshtein for whole doc
	dec.getcontext().prec = 10
	a=0
	for i in range(0,len(data)) :
		print i , len(data)
		sum2=0
		print i
		toks1=data[i].split(' ')
		for j in range(0,len(toks1)) :
			sum1=0
			for k in range(0,len(data)) :
				sum=0
				toks2=data[k].split(' ')
				ctr=0
				for m in range(0,len(toks2)) :
					if toks1[j].isalpha() and toks2[m].isalpha() :
						l=get_normlev_dist(toks1[j],toks2[m])
						sum=sum+l
						ctr=ctr+1
				if ctr>0 :
					sum=dec.Decimal(sum)/dec.Decimal(ctr)
				sum1=sum1+sum
			sum1=dec.Decimal(sum1)/dec.Decimal(len(data))
			sum2=sum2+sum1		
		sum2=dec.Decimal(sum2)/dec.Decimal(len(toks1))
		a=a+sum2
	a=dec.Decimal(a)/dec.Decimal(len(data))
	return a

#<-------------------------------DOC 2 VEC ---------------------------->



model1 = word2vec.Word2Vec(toklist1,size = 100, window = 300, min_count = 10, workers=4) #makes doc2vec model
model1_name = "tweetmodelword.txt"
model1.save(model1_name) 

#for similarity between data and each tweet from TOP-100
for i in range(0,len(toklist2)) :
	print model.docvecs.n_similarity(toklist1,toklist2[i]) # <--- Save this to file

#for similarity between each tweet in data and each tweet from TOP-100
for i in range(0,len(toklist1)) :
	for j in range(0,len(toklist2)) :
		print model.docvecs.n_similarity(toklist1[i],toklist2[j])  # <--- Save this to file

docvec1 = model.docvecs[99]
write_sim(outfile,tweets1,tweets2,model)		
#print model.docvecs.doesnt_match(docvec1)
print model1.most_similar_cosmul(positive=["htc"])





"""
	# Get Clusterwise Top terms	
	order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    	terms = vectorizer.get_feature_names()
	with open("results/new/"+str(topic)+"_cluster_terms"+str(n_clusters)+".csv",'w+') as f:
		for i in range(n_clusters):
			f.write("Cluster %d:\t" % i)
			for ind in order_centroids[i, :10]:
		    		f.write(' %s\t' % terms[ind])
			f.write("\n")
	f.close()

"""	
def hits(topic) :
#	link1 = "https://www.googleapis.com/customsearch/v1?key="+API_KEY+"&cx=017576662512468239146:omuauf_lfve&q="+topic
	link="http://in.search.yahoo.com/search?p="+topic	
	results = urllib.urlopen(link)
#	json_res = json.loads(results.read())
#	try :	
#		print json_res['queries']['request'][0]['totalResults']
#	   	google_hits=long(json_res['queries']['request'][0]['totalResults'])
	data=results.read()	
	start=data.find("Next</a><span>")
	data_endpart=data[start:] 
	end=data_endpart.find("results") 
	result=data[start+14:start+end-1]
	x=str(result)
	x=x.replace(',','')
#	x=google_hits
	print x
	#print google_hits
#	except KeyError :
#		print json_res
#		print("ERROR")
#		x=1
	try :
		a=math.log(long(x),2)
	except ValueError:
		a=0
	return a

def get_avg_rank(aspects_sel,aspect_hits) :
	x=[]
	done=[]
	l1=len(aspects_sel)
	l2=len(aspect_hits)
	for i in range(0,len(aspects_sel)) :
		y=[]
		done.append(aspects_sel[i][0])
		r1=l1-i
		j=util.get_index(aspect_hits,aspects_sel[i][0],0)
		if j!=-1 :
			y.append(aspects_sel[i][0])
			r2=l2-j
			r=int((r1+r2)/2)
			y.append(r)
			x.append(y)	
			
		
#	for i in range(0,len(aspect_hits)) :
#		if aspect_hits[i][0] in done :
#			t=1
#		else :
#			y=[]
#			done.append(aspect_hits[i][0])
#			y.append(aspect_hits[i][0])
#			r2=l2-i
#			j=util.get_index(aspects_sel,aspect_hits[i][0],0)
#			if j!=-1 :
#				r1=l1-j
#			else :
#				r1=0
#			r=int((r1+r2)/2)
#			y.append(r)
#			x.append(y)
	return x


def in_both(asp_hits,aspects_sel) :
	x=[]
	for i in range(0,len(aspects_sel)) :
		y=[]
		j=util.get_index(asp_hits,aspects_sel[i][0],0)
		if j!=-1 :
			y.append(aspects_sel[i][0])
			y.append(aspects_sel[i][1])
			y.append(asp_hits[j][1])
			x.append(y)
	return x
			
		
