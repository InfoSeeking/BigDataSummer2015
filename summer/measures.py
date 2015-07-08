import decimal as dec
import math

import sys

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
	tokens=[]
	for i in range(0,len(data)):
		toks1=data[i].split(' ')
		tokens.extend(toks1)
	utokens=list(set(tokens))
	for i in range(0,len(utokens)) :
		p=dec.Decimal(tokens.count(utokens[i]))/dec.Decimal(len(tokens))
		val=(p*log2(p))
		entropy=entropy-val
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
