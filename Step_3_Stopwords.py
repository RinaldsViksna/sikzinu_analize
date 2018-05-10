import sys
import io
import os
import json
import time
import classify_utils
from subprocess import *
import subprocess
import re


# argv[1] - filename to process
# using https://pypi.org/project/LatvianStemmer/1.0.1/#files
# processed file is saved in the same dir as source as filename_stemmed.tsv

def main():
    filename = os.path.splitext(sys.argv[1])[0]
    filename_clean = filename + "_stopwords.tsv"
    try:
        os.remove(filename_clean)
    except OSError:
        pass

    stopWords = []
    with open ('stopwords_garkaje.txt','rb') as stopWordsFile:
        for line in stopWordsFile:
            line = line.decode('utf-8-sig')
            stopWords.append(line.strip())

    with open(sys.argv[1],'rb') as f:
        for line in f:
            line = line.decode('utf-8')
            parts = line.split("\t")
            tweetText = parts[1]
            cleanText = ""

            # if there is punctuation, insert space between
            tweetText = re.sub(r'[.]+ ',' , ',tweetText)
            tweetText = re.sub(r'[,]+ ',' , ',tweetText)
            tweetText = re.sub(r'[?]+ ',' ? ',tweetText)
            tweetText = re.sub(r'[!]+ ',' ! ',tweetText)


            words = tweetText.split()
            for word in words:
                

                if (word not in stopWords):
                    cleanText = cleanText + " " + word
            # for stopWord in stopWords:
            #     # tweetText = re.sub(stopWord,' ',tweetText)
            #     tweetText = tweetText.replace(stopWord," ")
            # cleanText = tweetText


            clean_line = parts[0]+"\t"+cleanText+"\t"+parts[2]
            with open(filename_clean,'ab') as fout:
                fout.write(clean_line.encode("utf-8"))


# execute only if run as a script
if __name__ == "__main__":
    main()