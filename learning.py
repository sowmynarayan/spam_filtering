# This file is the learning phase of our more accurate code for spam detection

import re
import numpy as np

# Function to write a 2d list to a file in matrix form 

def print_to_file(mylist):
	opfile = open('output.txt','w')
	for i in mylist:
		for j in i:
			opfile.write(str(j)+" ")
		opfile.write("\n")
	opfile.close()

if __name__ == '__main__':
	input_file = 'train'
	
	# This is the count threshold value for a word to be considered feature. 
	# We select any word of freq > 50 as a feature. A lower word count gives
	# better predictions.
	min_word_count = 50
	f = open(input_file,'r')
	features_list = []
	rows = 0
	
	# Perl style regular exp that denotes a word followed by a number
	regex = re.compile('\S+ \d+')
	
	#First pass through the file and build the features list

	for line in f:
		rows += 1
		matchlist = regex.findall(line)
		for item in matchlist:
			wordval = re.split('\s+',item)
			if (int(wordval[1]) > min_word_count) and (wordval[0] not in features_list):
				features_list.append(wordval[0])
	cols = len(features_list)
	print "Number of features: ",len(features_list)
	f.close()
	print "Building feature table..."

	f2 = open('meta.txt','w')
	towrite = str(cols) + "\n"
	f2.write(towrite)
	for item in features_list:
		f2.write(item + "\n")
	f2.close()

	# Now count the occurence of each feature in each mail
	feature_table = [[0 for x in range(cols+1)] for y in range(rows)]
	
	f = open(input_file,'r')
	i = 0
	for line in f:
		str_to_match = '/\d+/\d+ (ham|spam)'
		spam_or_ham = re.search(str_to_match,line)
		if spam_or_ham:
			matchstring = spam_or_ham.group(1)
			if matchstring == 'spam':
				feature_table[i][0] = 'yes'
			elif matchstring == 'ham':
				feature_table[i][0] = 'no'
			else:
				feature_table[i][0] = 'unknown'
		i += 1
	f.close()
    
    # Now we have the feature table ready. Write this to a file which the second phase will read from
    
	f = open(input_file,'r')
	i = 0
	j = 1
	for line in f:
		for item in features_list:
			str_to_match = item + " (\d+)"
			matchcount = re.search(str_to_match,line)
			if matchcount:
				count = int(matchcount.group(1))
				feature_table[i][j] = count
			else:
				feature_table[i][j] = 0
			j += 1
		i += 1
		j = 1
	print_to_file(feature_table)
