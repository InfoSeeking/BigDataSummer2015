import os
from gensim.models import doc2vec,word2vec
import nltk
import util
import sys
import tagger


def make_word2vec_file(pos_tweets,file_name,merge) :
	stopwords=util.txtTolist("lists/stopwords.txt")
	y=[]
	pos_tweets=list(pos_tweets)
	for tweet in pos_tweets :
		x=[]
		for tok in tweet :
			if tok[1]=="A" or tok[1]=="N" or tok[1]=="^" or tok[1]=="V"  :
				x.append(tok[0])
			if tok[1]=="@" or tok[1]=="#" :
				x.append(tok[0].strip("#@"))
		x=[tok for tok in x if tok not in stopwords ]
		y.append(x)
	util.listTocsv(file_name,y)
	if merge :
		y=[item for sublist in y for item in sublist if item not in y ]
	return y

reload(sys)  
sys.setdefaultencoding("utf-8")

file_path1="data/tagged_data/data_HTC.csv"
file_name1=os.path.basename(file_path1)
file_name1=file_name1.strip("\n")
wfile_name1="TOK_"+file_name1

file_path2="results/HTC/HTC_KMEANS/TOP100_k_means25.txt"
file_name2=os.path.basename(file_path2)
file_name2=file_name2.strip("\n")
wfile_name2="TOK_"+file_name2

tweets1=util.txtTolist(file_path1)
pos_tweets1=tagger.runtagger_parse(tweets1)

tweets2=util.txtTolist(file_path2)
pos_tweets2=tagger.runtagger_parse(tweets2)

toklist1=make_word2vec_file(pos_tweets1,wfile_name1,True)
toklist2=make_word2vec_file(pos_tweets2,wfile_name2,False)

sentence=doc2vec.TaggedLineDocument(wfile_name1)
model = doc2vec.Doc2Vec(sentence,size = 100, window = 300, min_count = 10, workers=4)
model_name = "tweetmodel.txt"
model.save(model_name)
for i in range(0,len(toklist2)) :
	print model.docvecs.n_similarity(toklist1,toklist2[i])

  
