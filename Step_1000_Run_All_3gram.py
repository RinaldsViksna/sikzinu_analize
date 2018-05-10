import sys
import os
import json
import time
import nltk
import re
from itertools import islice
from sklearn import svm
from sklearn import naive_bayes
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy
import classify_utils

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

# Load tsv files and train classifiers
# argv[1] - filename to process

def main():
    ngrams = (1,3)
    tweets = []
    # priekš Stratified Cross-validation
    tweets_pos = []
    tweets_neu = []
    tweets_neg = []
    num_folds = 10
    start = time.time() # to get execution time
    """Load data file"""
    f = open(sys.argv[1],encoding="utf8") # pass data file as first parameter
    for line in f:
        try: 
            tweet = line.split("\t")
        except:
            pass
        #first is tweet id, [1] is text [2] is sentiment (POS,NEG,NEU)
        tweet_text = classify_utils.cleanup(tweet[1])
        # replace links from tweetText to avoid https:/ giving negative emoji
        tweet_text = re.sub(r'http(.*?)(\s|$)','_link ',tweet_text)
        tweet_sentiment = tweet[2].rstrip() # sentiments are last item on list, so they get \n added
        # append clean tweet to tweets list
        # do stratified CV, so all tweets ar split according to sentiment
        if tweet_sentiment == "POS":
            tweets_pos.append((tweet_text, tweet_sentiment))
        if tweet_sentiment == "NEU":
            tweets_neu.append((tweet_text, tweet_sentiment))
        if tweet_sentiment == "NEG":
            tweets_neg.append((tweet_text, tweet_sentiment))

    # Do 10-fold Cross-Validation.
    # initialize 2D dictionary to store confusion matrix
    classes = {"POS","NEG","NEU"}
    result_svm = {}
    for row in classes:
        result_svm[row] = result_svm.get(row,{})
        for col in classes:
            result_svm[row][col] = 0
    # initialize 2D dictionary to store confusion matrix
    result_nb = {}
    for row in classes:
        result_nb[row] = result_nb.get(row,{})
        for col in classes:
            result_nb[row][col] = 0
    # initialize 2D dictionary to store confusion matrix
    result_maxent = {}
    for row in classes:
        result_maxent[row] = result_maxent.get(row,{})
        for col in classes:
            result_maxent[row][col] = 0
    # initialize 2D dictionary to store confusion matrix
    result_nn = {}
    for row in classes:
        result_nn[row] = result_nn.get(row,{})
        for col in classes:
            result_nn[row][col] = 0
    # split all tweets in train and test sets
   
    for i in range(num_folds):
        print("fold #{0}\r".format(i),end=''),
        training_set = []
        training_y = []
        test_set = []
        test_y = []
        # For Stratified CV
        for index, tweet in enumerate(tweets_pos):
            if index % 10 == i:
                test_set.append(tweet[0])
                test_y.append(tweet[1])
            else:
                training_set.append(tweet[0])
                training_y.append(tweet[1])
        for index, tweet in enumerate(tweets_neu):
            if index % 10 == i:
                test_set.append(tweet[0])
                test_y.append(tweet[1])
            else:
                training_set.append(tweet[0])
                training_y.append(tweet[1])
        for index, tweet in enumerate(tweets_neg):
            if index % 10 == i:
                test_set.append(tweet[0])
                test_y.append(tweet[1])
            else:
                training_set.append(tweet[0])
                training_y.append(tweet[1])
        # Sparse feature vector
        vectorizer = CountVectorizer(ngram_range=ngrams)
        X_train = vectorizer.fit_transform(training_set)
        X_test = vectorizer.transform(test_set)
        # print(vectorizer.vocabulary_)
        print("size of vocabulary: " + str(len(vectorizer.vocabulary_)))
        print( take(25, vectorizer.vocabulary_) )

        SVMClassifier = svm.SVC(kernel="linear") # maybe svm.SVC(kernel="linear")
        SVMClassifier.fit(X_train,training_y)
        result_fold_svm = classify_utils.testModelConfusion(SVMClassifier,X_test,test_y)
        result_svm = classify_utils.addMatrix(result_svm, result_fold_svm)

        NBClassifier = naive_bayes.MultinomialNB()
        NBClassifier.fit(X_train,training_y)
        result_fold_nb = classify_utils.testModelConfusion(NBClassifier,X_test,test_y)
        result_nb = classify_utils.addMatrix(result_nb, result_fold_nb)

        MaxentClassifier = LogisticRegression()
        MaxentClassifier.fit(X_train,training_y)
        result_fold_maxent = classify_utils.testModelConfusion(MaxentClassifier,X_test,test_y)
        result_maxent = classify_utils.addMatrix(result_maxent, result_fold_maxent)

        NNClassifier = MLPClassifier()
        NNClassifier.fit(X_train,training_y)
        result_fold_nn = classify_utils.testModelConfusion(NNClassifier,X_test,test_y)
        result_nn = classify_utils.addMatrix(result_nn, result_fold_nn)

    print(result_svm)
    accuracy_svm = classify_utils.getAccuracy(result_svm)
    f1_svm = classify_utils.getF1(result_svm)
    # print("total Features used "+str(len(featureList)))
    print("accuracy svm is "+ str(accuracy_svm))
    print("f1 svm is "+ str(f1_svm))

    print(result_nb)
    accuracy_nb = classify_utils.getAccuracy(result_nb)
    f1_nb = classify_utils.getF1(result_nb)
    print("accuracy nb is "+ str(accuracy_nb))
    print("f1 nb is "+ str(f1_nb))

    print(result_maxent)
    accuracy_maxent = classify_utils.getAccuracy(result_maxent)
    f1_maxent = classify_utils.getF1(result_maxent)
    print("accuracy maxent is "+ str(accuracy_maxent))
    print("f1 maxent is "+ str(f1_maxent))

    print(result_nn)
    accuracy_nn = classify_utils.getAccuracy(result_nn)
    f1_nn = classify_utils.getF1(result_nn)
    print("accuracy nn is "+ str(accuracy_nn))
    print("f1 nn is "+ str(f1_nn))

    print("average accuracy:"+str((accuracy_svm+accuracy_nb+accuracy_maxent+accuracy_nn)/4))
    print("average f1:"+str((f1_svm+f1_nb+f1_maxent+f1_nn)/4))

    end = time.time()
    print( "Process took "+str(end-start)+".")

# execute only if run as a script
if __name__ == "__main__":
    main()


