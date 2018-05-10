import re
import sys
import os

# How many are correctly predicted/all
def getAccuracy (confusionMatrix):
    accuracy = 0
    correct = 0
    total = 0
    for row, cols in confusionMatrix.items():
        for col in cols:
            if row == col:
                correct = correct + confusionMatrix[row][col]
            total = total + confusionMatrix[row][col]
    accuracy = 0 if total == 0 else correct / total
    return accuracy

def getF1 (confusionMatrix):
    """
    Aprēķina F1
    https://stats.stackexchange.com/questions/51296/how-do-you-calculate-precision-and-recall-for-multiclass-classification-using-co
    """
    f1 = 0
    rows = len(confusionMatrix) #actual; len = number of classes
    precision = 0
    recall = 0
    for row, cols in confusionMatrix.items():
        truePositive = 0
        tPFP = 0
        tPFN = 0
        for col in cols:
            if row == col:
                truePositive = confusionMatrix[row][col]
            tPFP = tPFP + confusionMatrix[col][row]
            tPFN = tPFN + confusionMatrix[row][col]
        precision = precision if tPFP == 0 else precision + truePositive / tPFP
        recall = recall if tPFN == 0 else recall + truePositive / tPFN 
    precision = precision / rows
    recall = recall / rows
    f1 = 2 * precision * recall / (precision + recall)
    return f1

def cleanup(text):
    # text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',text)
    # text = re.sub(r'[\.,!?\[\]{}"\'<>/\n\r\t]',' ',text)
    # text = re.sub('\s{2,}', ' ', text)
    # return text.lower().decode("utf8")
    return text

def getFeatureVector(tweetText):
    """No longer used"""
    featureVector = []
    #split tweet into words
    words = tweetText.split()
    for w in words:
        #check if the word stats with an alphabet
        val = re.search(r"[@#]", w)
        #ignore if it is a stop word or hashtag
        # if ((stopWords.getitem(w)==0) and val is None):
        # if (val is None):
        featureVector.append(w)
    return featureVector

def addMatrix(confusionMatrix, matrix_two):
    """Sums two matrices and returns sum"""
    for row, cols in confusionMatrix.items():
        for col in cols:
            confusionMatrix[row][col] = confusionMatrix[row][col] + matrix_two[row][col]
    return confusionMatrix

def testModelConfusion(Classifier,X_test,test_y):
    """ Test given classifier, return confusion matrix
        Input Classifier, list with test data, list with target classes
    """
    # initialize 2D dictionary to store confusion matrix
    classes = {"POS","NEG","NEU"}
    result = {}
    for row in classes:
        result[row] = result.get(row,{})
        for col in classes:
            result[row][col] = 0

    prognoses = Classifier.predict(X_test)
    for index, actual in enumerate(test_y):
        prognosis = prognoses[index]
        result[actual][prognosis] = result[actual][prognosis] + 1
    return result
