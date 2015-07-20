from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import doc2vec,word2vec

import decimal as dec
import math
import sys
import os
import csv

import util
import paraphrase
import tagger





reload(sys)  
sys.setdefaultencoding('utf8')


def log2(a):
	num=math.log10(a)
	den=math.log10(2)
	val=dec.Decimal(num)/dec.Decimal(den)
	return val
	

def entropy(data) :
	dec.getcontext().prec = 10
	entropy=0
	allWords=[]
	for i in range(0,len(data)):
		words=data[i].split(' ')
		allWords.extend(words)
	words=list(set(allWords)) 
	for word in words :
		p=dec.Decimal(allWords.count(word))/dec.Decimal(len(allWords))
		entropy=entropy-(p*log2(p))
	return entropy
		

def get_normdist(word1,word2):
	n=len(word1)
	m =len(word2)
	if n > m:
		return get_normdist(word2,word1)
	else :
		curr = [i for i in range(n+1)]
		for i in range(1,m+1):
			prev=curr
			curr=[0]*(n+1)
			curr[0]=i
			for j in range(1,n+1):
				add=prev[j]+1
				delete=curr[j-1]+1
				change=prev[j-1]
				if word1[j-1] != word2[i-1]:
					change = change + 1
				curr[j] = min(add, delete, change)
		val=dec.Decimal(curr[n])/dec.Decimal(len(word1)*len(word2))
		return val


def levenshtein(data) :
	sum=0
	for i in range(0,len(data)) :
		j=len(data)-1
		while j> i :
			a=get_normdist(data[i],data[j])
			sum=dec.Decimal(sum+a)
			j=j-1
	den=(len(data)*(len(data)-1))/2	
	val=dec.Decimal(sum)/dec.Decimal(den)
	return val


def get_ParaphraseSim(source,rfile,outPath,topic,k) :
	topk="_TOP_"+str(k)
	ind=outPath.rfind("/")
	outfile1=outPath[0:ind]+"/"+topic+topk+"_ParaphraseDocwiseResults.csv"
	
	s="\t"
	for i in range(0,len(source)):
		s=s+str(source[i].replace("\n"," "))
	s=s.lstrip("\t")	
	
	target=paraphrase.readInData(rfile)
	paraphrase.write_features(rfile,outfile1,s,target)
	
	rfilename=os.path.basename(rfile).rstrip(".txt")
	outfile2=outPath+"/"+rfilename+"_ParaphraseTweetwiseResults.csv"
	paraphrase.write_features_matrix(outfile2,target)

def cosineSim(allTweets,result) :
	vectorizer = TfidfVectorizer()
	X = vectorizer.fit_transform(allTweets)
	i=allTweets.index(result)
	v=cosine_similarity(X, X[i:i+1])
	return str(sum(v[0])/len(v[0]))
	
def writeCosineSimMatrix(outFile,allTweets,results) :
	vectorizer = TfidfVectorizer()
	X = vectorizer.fit_transform(allTweets)
	with open(outFile, "a+") as fp :
     		writeFile = csv.writer(fp)
		for result in results :
			i=allTweets.index(result)
			sim=cosine_similarity(X, X[i:i+1])
			writeFile.writerow(sim)


def get_VSMsim(rfile,allTweets,results) :
	rfilename=os.path.basename(rfile).rstrip(".txt")
	sim=[]
	sim.append(rfilename)
	for result in results :
		sim.append(cosineSim(allTweets,result))
	return sim

#Selects relevant words to make vector : 
# Output list Format : if merge==False : [[w1,w2],[w1,w2,w3]] where [w1,w2] are words from doc 1 and [w1,w2,w3] are words from doc 2
# Output list Format : if merge==True : [w1,w2,w3] where [w1,w2] are words from doc 1 and [w1,w2,w3] are words from doc 2

def makeDoc2vecFile(pos_tweets,outfile,merge) :
	stopwords=util.txtTolist("lists/stopwords.txt")
	y=[]	
	for tweet in pos_tweets :
		x=[tok[0].strip("@#") for tok in tweet if tok[1]=="A" or tok[1]=="N" or tok[1]=="^" or tok[1]=="V" or tok[1]=="@" or tok[1]=="#" ]
		x=[tok for tok in x if tok not in stopwords ]
		y.append(x)
		with open(outfile,"a+") as f :
			for xi in x :
				f.write(str(xi)+" ")
			f.write("\n")
	if merge :
		y=[item for sublist in y for item in sublist if item not in y ]
	return y

def writeDoc2vecSimMatrix(outfile,allTweets,results,create) :
	if create :
		outfile1=os.path.dirname(outfile)+"/Doc2vecModelTokens.txt"
		pos_tweets=tagger.runtagger_parse(allTweets) #tokenizer and POS-tagger
		tokens=makeDoc2vecFile(pos_tweets,outfile1,False)
		sentence=doc2vec.TaggedLineDocument(outfile1) #Imports in doc2vec format
		model = doc2vec.Doc2Vec(sentence,size = 100, window = 300, min_count = 10, workers=4) #makes doc2vec model
		model_name = os.path.dirname(outfile)+"/Doc2vecModel.txt"
		model.save(model_name)	
	else :
		model_name = os.path.dirname(outfile)+"/Doc2vecModel.txt"	
		model=doc2vec.Doc2Vec.load(model_name)
	for i in range(0,len(allTweets)) :
		x=[]
		for result in results :
			k=allTweets.index(result)
			x.append(str(model.docvecs.similarity(i,k)))
		with open(outfile, "a+") as f :
		   	writeFile = csv.writer(f)
			writeFile.writerow(x)



