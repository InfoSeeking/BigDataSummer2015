# Uses CMU Noah's Ark Lab POS Tagger for tweets http://www.ark.cs.cmu.edu/TweetNLP/

import subprocess
import shlex
import csv
import sys  

RUN_TAGGER_CMD = "java -XX:ParallelGCThreads=2 -Xmx500m -jar ark-tweet-nlp-0.3.2.jar"


def _split_results(rows):
    for line in rows:
        line = line.strip()  # remove '\n'
        if len(line) > 0:
            if line.count('\t') == 2:
                parts = line.split('\t')
#		return parts
                tokens = parts[0]
                tags = parts[1]
                confidence = float(parts[2])
                yield tokens, tags, confidence


def _call_runtagger(tweets, run_tagger_cmd=RUN_TAGGER_CMD):
    tweets_cleaned = [tw.replace('\n', ' ') for tw in tweets]
    message = "\n".join(tweets_cleaned)
    message = message.encode('utf-8')
    args = shlex.split(run_tagger_cmd)
    args.append('--output-format')
    args.append('conll')
    po = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = po.communicate(message)
    pos_result = result[0].strip('\n\n')  # get first line, remove final double carriage return
    pos_result = pos_result.split('\n\n')  # split messages by double carriage returns
    pos_results = [pr.split('\n') for pr in pos_result]  # split parts of message by each carriage return
    return pos_results


def runtagger_parse(fname, run_tagger_cmd=RUN_TAGGER_CMD):
	with open(fname, 'rb') as f:
		reader = csv.reader(f)
		mylist = list(reader)
	f.close()
	tweets=[]		
	for row in mylist:
		tweets.append(str(row[0]))	
	pos_raw_results = _call_runtagger(tweets, run_tagger_cmd)
    	pos_result = []
    	for pos_raw_result in pos_raw_results:
        	pos_result.append([x for x in _split_results(pos_raw_result)])
    	return pos_result
	