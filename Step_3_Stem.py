import sys
import io
import os
import json
import time
import LatvianStemmer
import classify_utils

# argv[1] - filename to process
# using https://pypi.org/project/LatvianStemmer/1.0.1/#files
# processed file is saved in the same dir as source as filename_stemmed.tsv

def main():
    filename = os.path.splitext(sys.argv[1])[0]
    filename_stemmed = filename + "_stemmed.tsv"
    try:
        os.remove(filename_stemmed)
    except OSError:
        pass

    with open(sys.argv[1],'rb') as f:
        for line in f:
            line = line.decode('utf-8')
            parts = line.split("\t")
            tweetText = parts[1]
            tokens = classify_utils.getFeatureVector(tweetText)
            stemmed_tokens = ""
            for token in tokens:
                stemmed_token = LatvianStemmer.stem(token) 
                stemmed_tokens = stemmed_tokens + " "+ stemmed_token
            stemmed_line = parts[0]+"\t"+stemmed_tokens+"\t"+parts[2]
            with open(filename_stemmed,'ab') as ftrain:
                ftrain.write(stemmed_line.encode("utf-8"))


# execute only if run as a script
if __name__ == "__main__":
    main()