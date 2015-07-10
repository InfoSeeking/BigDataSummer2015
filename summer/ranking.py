import util
import urllib
import json
from decimal import Decimal, getcontext
import math
import csv

API_KEY="AIzaSyAAfn_jubdzVcDX0S7V7oSkq87wUOnL-Q8"

def get_freq(aspects) :
	allaspects=[]
	asp_freq=[]
	for aspect_tweet in aspects :
		for aspect in aspect_tweet :
			if aspect in allaspects :
				ind=allaspects.index(aspect)			
				asp_freq[ind][1]=asp_freq[ind][1]+1
			else :
				x=[]
				x.append(aspect)
				x.append(int(1))
				allaspects.append(aspect)
				asp_freq.append(x)

	return asp_freq

def hits(topic) :
#	link1 = "https://www.googleapis.com/customsearch/v1?key="+API_KEY+"&cx=017576662512468239146:omuauf_lfve&q="+topic
	link1="http://in.search.yahoo.com/search?p="+topic	
	print link1	
	print("\n")
	results = urllib.urlopen(link1)
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

def get_pmi(num,hits_a,hits_t) :
	den=hits_a+hits_t
	if den!=0 :
		ratio=34.000000+num-den
	else :
		ratio=0
		val=0
	return ratio

def pmi_list(aspects,target,file_path) :
	pmis=[]
	pmi=["NULL"]*3
	hits_t=hits(target)
	for i in range(0,len(aspects)) :
		pmi[0]=aspects[i]
		pmi[1]=target
		num=hits(target+'+'+aspects[i])
		hits_a=hits(aspects[i])
		pmi[2]=float(get_pmi(num,hits_a,hits_t))
		print i 
		print len(aspects)
		print pmi[2]
		pmis.append(pmi)
		dataStrip = []	
		dataStrip.append(pmi[0])
		dataStrip.append(pmi[2])
		with open(file_path, "a+") as fp :
			writeFile = csv.writer(fp)
	   		writeFile.writerow(dataStrip)
		fp.close()
	return pmis


def hitswise(aspects,topic,file_path) :
	asphits=[]
	asphit=["NULL"]*2
	for i in range(0,len(aspects)) :
		print i
		asphit[0]=aspects[i][0]
		asphit[1]=hits(aspects[i][0],topic,file_path)
		asphits.append(asphit)
	return asphits


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
	l1=len(aspects_sel)
	l2=len(asp_hits)
	for i in range(0,l1) :
		y=[]
		j=util.get_index(asp_hits,aspects_sel[i][0],0)
		if j!=-1 :
			y.append(aspects_sel[i][0])
			y.append(aspects_sel[i][1])
			y.append(asp_hits[j][1])
			x.append(y)
	return x
			
		
