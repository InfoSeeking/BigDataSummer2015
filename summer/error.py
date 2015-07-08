import util
	
def has_no_alpha(aspects):
	for aspect in aspects :
		if aspect[0].strip("@#*!$%^&\"\',.{}[]()-\\+=_/:\t\n")=="" :
			print(str(aspect)+" removedc")
			aspects.remove(aspect)
	return aspects

def group_same(aspects) :
	for i in range(0,len(aspects)) :
		print i
		aspects[i][0]=aspects[i][0].strip("#@")
		token=aspects[i][0].rstrip("'s")
		j=0
		nf=True
		while j<i and nf :
			if token.lower() in aspects[j][0].lower() :
				print("entered 1")
				aspects[j][1]=aspects[j][1]+aspects[i][1]
				aspects[i][1]=0
				nf=False
			elif aspects[j][0].lower() in token.lower() :
				print("entered 1")
				aspects[j][0]=token
				aspects[j][1]=aspects[j][1]+aspects[i][1]
				aspects[i][1]=0
				nf=False
			else :
				j=j+1
	aspects=sorted(aspects,key=lambda x: int(x[1]),reverse=True)
	aspects=util.filter_rlist(aspects,1,1)	
	print aspects
	return aspects	
				

def correct(aspects) :
	aspects=has_no_alpha(aspects)
	aspects=group_same(aspects)
	return aspects	
