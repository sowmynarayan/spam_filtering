To run the spam filtering code the test and training data set files named 'test' and 'train'
 must be placed in the same directory as the code.

We have two programs: one which will consider just the occurence of the word as a feature (less runtime 
but less accurate)  and second which will consider number of occurences as the feature (more time and 
more accurate)

1. TO RUN NAIVE BAYESIAN SPAM FILTER WITH WORD OCCURANCE AS FEATURE:

Copy train and test to same directory as code
Execute the command:

$ python spam_filter.py 

Output from above will be stored in results.txt file
Overall runtime is less than 10s.

2. TO RUN SPAM FILTER WITH NUMBER OF OCCURENCES AS FEATURE:

First execute:
$ python learning.py 

After learning phase is complete and decision table is built:
$ python detect.py 

Runtime is around 80s for learning and more than 100s for detection phase.
