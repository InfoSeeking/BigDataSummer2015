import csv
import error
import math

def txtTolist(myfile): #repeats=True remove repetitons from final list
	with open(myfile) as f:
    		mylist=[line.rstrip('\n') for line in f]
	return mylist

def csvTolist(myfile) :
	with open(myfile, 'rb') as f:
		reader = csv.reader(f)
		mylist = list(reader)
	return mylist

def csvColTolist(myfile,i) :
	myCol=[]
	mylist=csvTolist(myfile)	
	for row in mylist:
		myCol.append(str(row[i]))
	return myCol
	
	
def listTocsv(file_path,mylist):
	with open(file_path,'w+') as f:	
		wr = csv.writer(f)
		wr.writerows(mylist)

def get_index(mylists,tok,i) :
	for mylist in mylists :
		if mylist[i]==tok :
			return int(mylists.index(mylist))
		else :
			return int(-1)
		

def is_in_file(myfile,word,err_check) :
	in_file=False
	if word in open(myfile).read() :
		in_file=True
	else :
		if err_check :
			in_file=error.is_in_file(myfile,word)
	return in_file



def filter_rlist(ranked_list,lim,ctr) : #list has to be ranked decreasingly
	repeats=False
	ranked_list=[x for x in ranked_list if x[ctr]>=lim ]
	if repeats:
		ranked_list=list(set(ranked_list))	
	return ranked_list

def log2( x ):
	num=math.log10(x)
	den=math.log10(2)
	ratio=num/den
	return ratio

def listfromlist(x,ind):
	y=[tok[ind] for tok in x ]
	return y

def remove_ind(mylist,ind) : #ind is a list of indices to remove from mylist
	if len(ind)>0 :
		for i in ind :
			x.append(mylist[i])
		for tok in x :
			mylist.remove(tok)
	return  mylist
