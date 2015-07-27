import numpy as np
from numpy import prod
import time

if __name__ == "__main__":

    starttime = time.time()
    file_content = open('train', 'r')
    
    # Dictionaries of key-value pairs to store the word counts of spam and ham features
    spam_wc = {}
    ham_wc = {}
    feature_def = []
    data_line = file_content.readline()

    # Initalized to 1 for Laplace smoothing
    total_size = 1
    yes_size = 1
    no_size = 1

    # Convert the traininf data set file into a list of features to learn from
    while data_line:
        splitter = data_line.split(' ')

        total_size += 1
        if splitter[1] == 'spam':
            yes_size += 1
        if splitter[1] == 'ham':
            no_size += 1

        # print splitter[0]
        feature_line = splitter[2:]
        items = iter(feature_line)
        for x in items:
            if splitter[1] == 'spam':
                spam_wc[x] = 1 + spam_wc.get(x, 1) # Default value set to 1 for smoothing
            if splitter[1] == 'ham':
                ham_wc[x] = 1 + ham_wc.get(x, 1) # Default value set to 1 for smoothing
        data_line = file_content.readline()

    file_content.close()

    # Now we have ready the list of spam and ham features
    print 'Training data processed, total records is ', total_size-1

    
    test_results = []
    inferred_results = []
    file_content = open('test', 'r')
    data_line = file_content.readline()
    
    # Actual bayesian probability stuff 
    # We can calculate P(spam|word) to tell if given mail is spam or ham

    while data_line:
        yes_prob = [float(yes_size) / float(total_size)]
        no_prob = [float(no_size) / float(total_size)]
        splitter = data_line.split(' ')
        test_results.append(splitter[1])
        words = splitter[2::2]
        
        # Calculate P(yes) , P(no) , P(spam|word) , P(ham|word)
      
        for word in words:
            yes_prob.append(float(spam_wc.get(word, 0)))
            no_prob.append(float(ham_wc.get(word, 0)))
        yes_prob = np.array(yes_prob) / yes_size
        no_prob = np.array(no_prob) / no_size
        if prod(yes_prob) > prod(no_prob):
            inferred_results.append('spam')
        else:
            inferred_results.append('ham')
        data_line = file_content.readline()
    file_content.close()

    #print spam_wc
    #print ham_wc
    print "Please check results.txt file for inferred results"
    #print "Actual   : ", test_results
    #print "Inferred : ", inferred_results
    
    results = open('results.txt','w')
    for item in inferred_results:
        results.write(item+"\n")
    results.close()

    # Compare and display % of correct results with the actual answers
    
    correct_predictions = 0
    for k in range(len(inferred_results)):
        if inferred_results[k] == test_results[k]:
            correct_predictions += 1
    print "Predicted ", (float(correct_predictions) / float(len(inferred_results))) * 100, "% of results correctly."
    runtime = time.time() - starttime
    print "Runtime ",runtime,"s."
