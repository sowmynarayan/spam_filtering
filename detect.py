# This file is the second detection phase of our more accurate spam detection

import re
import numpy as np
import time

# Function to read matrix from a file as a 2d list

def file_to_array():
	opfile = open('output.txt','r')
	data = [[n for n in line.split()] for line in opfile]
	return data

# To print a 2d list with proper indentation

def print_2d(mylist):
	for i in range(len(mylist)):
		for j in range(len(mylist[i])):
			print mylist[i][j] ,
		print

if __name__ == '__main__':
    
	starttime = time.time()
	fname = 'test'
	f2 = open('meta.txt','r')
	numfeatures = int(f2.readline())
	feature_list = [line.rstrip('\n') for line in f2]
	f2.close()

	numlines = 0
	numyes = 0
	numno = 0
	f_given_yes = 0
	p_of_feature_yes = [0.0 for x in range(numfeatures)]
	
	# Perl style regular exp that denotes a word followed by a number
	regex = re.compile('\S+ \d+')

	result = []
	featureword_list = []
	i = 0
	datafile = open(fname,'r')
	f = open('output.txt','r')
	
	# Parse the test data file and build the list of feature words
	for data in datafile:
		featurewords = []
		matchlist = regex.findall(data)
		if 'spam' in data:
			result.append('Spam')
		else:
			result.append('Ham')
		for thing in matchlist:
			wordval = re.split('\s+',thing)
			if (wordval[0] in feature_list) and  (wordval[0] not in featurewords):
				index = feature_list.index(wordval[0])
				featurewords.append((int(index),int(wordval[1])))
		#print(featurewords)
		featureword_list.append(featurewords)
		i += 1
	
	feature_table = file_to_array()
	feature_table = np.array(feature_table)

	feature_yes = feature_table[np.where(feature_table[:,0] == 'yes')]
	feature_no = feature_table[np.where(feature_table[:,0] == 'no')]
	
	feature_yes = feature_yes[:,1:].astype(int)
	feature_no = feature_no[:,1:].astype(int)
	
	decision = []
	
	# Now we have a list of feature words so calc P(yes) P(no)
	for record in featureword_list:
		# Each data to decide
		
		#Sampling of total
		total_yes = len(feature_yes) + 1
		total_no = len(feature_no) + 1
		
		(total_no, temp) = feature_no.shape
		prob_yes = float(total_yes) / float(total_yes+total_no)
		prob_no = 1 - prob_yes
		
		for tuple in record:
		    # Yes if count of word in test data is larger than than that in spam.
			(count_yes, temp) = feature_yes[np.where(feature_yes[:,tuple[0]] >= tuple[1])].shape
			(count_no, temp) = feature_no[np.where(feature_no[:,tuple[0]] >= tuple[1])].shape
			
			#Smoothing
			count_yes = count_yes + 1
			count_no = count_no + 1
			
			prob_yes = prob_yes * float(count_yes)/float(total_yes)
			prob_no = prob_no * float(count_no)/float(total_no)
 		if prob_yes > prob_no:
			print "Spam !"
			decision.append('Spam')
		else:
			print "Ham !"
			decision.append('Ham')

    # Find the % of correct predictions
	correct_predictions = 0
	for k in range(len(decision)):
		if decision[k] == result[k]:
			correct_predictions += 1
	print " Predicted ", (float(correct_predictions)/float(len(decision)))*100, "% of results correctly."
	f.close()
	runtime = time.time() - starttime
	print "Runtime: ",runtime,"s."
