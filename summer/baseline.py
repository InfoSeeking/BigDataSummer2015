from __future__ import division
import util
import sys
import random

import nltk
from nltk.tokenize import word_tokenize
from nltk.classify import MaxentClassifier
from nltk.stem import porter

from cPickle import load
from cPickle import dump

from collections import *


# sub-functions for find overlapping n-grams
def intersect_modified (list1, list2) :
    cnt1 = Counter()
    cnt2 = Counter()
    for tk1 in list1:
        cnt1[tk1] += 1
    for tk2 in list2:
        cnt2[tk2] += 1    
    inter = cnt1 & cnt2
    union = cnt1 | cnt2
    largeinter = Counter()
    for (element, count) in inter.items():
        largeinter[element] = union[element]
    return list(largeinter.elements())

def intersect (list1, list2) :
    cnt1 = Counter()
    cnt2 = Counter()
    for tk1 in list1:
        cnt1[tk1] += 1
    for tk2 in list2:
        cnt2[tk2] += 1    
    inter = cnt1 & cnt2
    return list(inter.elements())



    
# create n-gram features and stemmed n-gram features
def paraphrase_Das_features(source, target):
    	
    source_words = source.split(" ")
    target_words = target.split(" ")
	
    features = {}
    
    ###### Word Features ########
	
    s1grams = [w.lower().encode("utf-8") for w in source_words]
    t1grams = [w.lower().encode("utf-8") for w in target_words]
    s2grams = []
    t2grams = []
    s3grams = []
    t3grams = []
        
    for i in range(0, len(s1grams)-1) :

        if i < len(s1grams) - 1:
            s2gram = s1grams[i] + " " + s1grams[i+1]
            s2grams.append(s2gram)
        if i < len(s1grams)-2:
            s3gram = s1grams[i] + " " + s1grams[i+1] + " " + s1grams[i+2]
            s3grams.append(s3gram)
            
    for i in range(0, len(t1grams)-1) :
        if i < len(t1grams) - 1:
            t2gram = t1grams[i] + " " + t1grams[i+1]
            t2grams.append(t2gram)
        if i < len(t1grams)-2:
            t3gram = t1grams[i] + " " + t1grams[i+1] + " " + t1grams[i+2]
            t3grams.append(t3gram)

    f1gram = 0        
    precision1gram = len(set(intersect(s1grams, t1grams))) / len(set(s1grams))
    recall1gram    = len(set(intersect(s1grams, t1grams))) / len(set(t1grams))
    if (precision1gram + recall1gram) > 0:
        f1gram = 2 * precision1gram * recall1gram / (precision1gram + recall1gram)
    precision2gram = len(set(intersect(s2grams, t2grams))) / len(set(s2grams))
    recall2gram    = len(set(intersect(s2grams, t2grams))) / len(set(t2grams))
    f2gram = 0
    if (precision2gram + recall2gram) > 0:
        f2gram = 2 * precision1gram * recall2gram / (precision2gram + recall2gram)
    precision3gram = len(set(intersect(s3grams, t3grams))) / len(set(s3grams))
    recall3gram    = len(set(intersect(s3grams, t3grams))) / len(set(t3grams))
    f3gram = 0
    if (precision3gram + recall3gram) > 0:
        f3gram = 2 * precision3gram * recall3gram /(precision3gram + recall3gram)

    features["precision1gram"] = precision1gram
    features["recall1gram"] = recall1gram
    features["f1gram"] = f1gram
    features["precision2gram"] = precision2gram
    features["recall2gram"] = recall2gram
    features["f2gram"] = f2gram
    features["precision3gram"] = precision3gram
    features["recall3gram"] = recall3gram
    features["f3gram"] = f3gram
    
    ###### Stemmed Word Features ########
    
    porterstemmer = porter.PorterStemmer()
    
    s1stems = [porterstemmer.stem(w.lower().encode("utf-8")) for w in target_words if w.isalpha()]
    t1stems = [porterstemmer.stem(w.lower().encode("utf-8")) for w in target_words if w.isalpha()]
    s2stems = []
    t2stems = []
    s3stems = []
    t3stems = []
        
    for i in range(0, len(s1stems)-1) :
        if i < len(s1stems) - 1:
            s2stem = s1stems[i] + " " + s1stems[i+1]
            s2stems.append(s2stem)
        if i < len(s1stems)-2:
            s3stem = s1stems[i] + " " + s1stems[i+1] + " " + s1stems[i+2]
            s3stems.append(s3stem)
            
    for i in range(0, len(t1stems)-1) :
        if i < len(t1stems) - 1:
            t2stem = t1stems[i] + " " + t1stems[i+1]
            t2stems.append(t2stem)
        if i < len(t1stems)-2:
            t3stem = t1stems[i] + " " + t1stems[i+1] + " " + t1stems[i+2]
            t3stems.append(t3stem)
                
    precision1stem = len(set(intersect(s1stems, t1stems))) / len(set(s1stems))
    recall1stem    = len(set(intersect(s1stems, t1stems))) / len(set(t1stems))
    f1stem = 0
    if (precision1stem + recall1stem) > 0:
        f1stem = 2 * precision1stem * recall1stem / (precision1stem + recall1stem)
    precision2stem = len(set(intersect(s2stems, t2stems))) / len(set(s2stems))
    recall2stem    = len(set(intersect(s2stems, t2stems))) / len(set(t2stems))
    f2stem = 0
    if (precision2stem + recall2stem) > 0:
        f2stem = 2 * precision2stem * recall2stem / (precision2stem + recall2stem)
    precision3stem = len(set(intersect(s3stems, t3stems))) / len(set(s3stems))
    recall3stem    = len(set(intersect(s3stems, t3stems))) / len(set(t3stems))
    f3stem = 0
    if (precision3stem + recall3stem) > 0:
        f3stem = 2 * precision3stem * recall3stem / (precision3stem + recall3stem)
	
    features["precision1stem"] = precision1stem
    features["recall1stem"] = recall1stem
    features["f1stem"] = f1stem
    features["precision2stem"] = precision2stem
    features["recall2stem"] = recall2stem
    features["f2stem"] = f2stem
    features["precision3stem"] = precision3stem
    features["recall3stem"] = recall3stem
    features["f3stem"] = f3stem

    return features


# read from train/test data files and create features
def readInData(filename):

    data = util.txtTolist(filename)
    return data
    

             
if __name__ == "__main__":
	reload(sys)  
	sys.setdefaultencoding('utf8')
	topics=["HTC","Uber","Samsung","Beyonce","Obama"]
	for topic in topics :
		print topic 
		outfile="results/new/"+topic+"_PrecisionRecallResults.csv"
		source = readInData("data/tagged_data/data_"+topic+".txt")
		s="\t"
		for i in range(0,len(source)):
			s=s+str(source[i].replace("\n"," "))
		s=s.lstrip("\t")	
		
		print "Calculating for Clustering Results"
		k=[5,10,25,50,100]
		for ki in k :
			infile="results/new/"+topic+"/KMEANS/"+topic+"_TOP100_k_means"+str(ki)+".txt"
			target  = readInData(infile)
			t="\t"
			for i in range(0,len(target)):
				t=t+str(target[i].replace("\n"," "))
			features = paraphrase_Das_features(s,t.lstrip("\t"))
			with open(outfile,"a+") as f:
				f.write(infile+"\n"+str(features)+"\n")
			
		
		print "Calculating for RANDOM_TOP_100 results"
		target  = source[0:100]
		t="\t"
		for i in range(0,len(target)):
			t=t+str(target[i].replace("\n"," "))
		features = paraphrase_Das_features(s,t.lstrip("\t"))
		with open(outfile,"a+") as f:
			f.write(infile+"\n"+str(features)+"\n")
		
		print "Calculating for ASPECT RANKING_ALGO TOP_100 results"
		infile="results/new/"+topic+"/ASPECT_RANKING/GREEDY1_"+str(topic)+".txt"
		target  = readInData(infile)
		t="\t"
		for i in range(0,len(target)):
			t=t+str(target[i].replace("\n"," "))
		features = paraphrase_Das_features(s,t.lstrip("\t"))
		with open(outfile,"a+") as f:
			f.write(infile+"\n"+str(features)+"\n")
		
		infile="results/new/"+topic+"/ASPECT_RANKING/GREEDY3_"+str(topic)+".txt"
		target  = readInData(infile)
		t="\t"
		for i in range(0,len(target)):
			t=t+str(target[i].replace("\n"," "))
		features = paraphrase_Das_features(s,t.lstrip("\t"))
		with open(outfile,"a+") as f:
			f.write(infile+"\n"+str(features)+"\n")
		
		
