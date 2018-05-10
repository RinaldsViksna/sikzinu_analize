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
    filename_stemmed = filename + "_lemmed.tsv"
    try:
        os.remove(filename_stemmed)
    except OSError:
        pass

    # print(result)
    with open(sys.argv[1],'rb') as f:
        for line in f:
            line = line.decode('utf-8')
            parts = line.split("\t")
            tweetText = parts[1]
            # remove links from tweetText
            tweetText = re.sub(r'http(.*?)(\s|$)','',tweetText)
            
            # save text to temp file for analysis wiht LVTagger
            tempfile = 'D:\\korpusi\\tempfile_stemmer.txt'
            tempfile_analyzed = "D:\\korpusi\\tempfile_stemmer_a.txt"
            try:
                os.remove(tempfile)
            except OSError:
                pass
            with open(tempfile,'ab') as tmp:
                tmp.write(tweetText.encode("utf-8"))

            command = 'java -jar tagger-1.0.0-jar-with-dependencies.jar <'+tempfile+' >'+tempfile_analyzed
            # print(command)
            os.system(command)

            stemmed_tokens = ""
            with open(tempfile_analyzed,'rb') as fan:
                for line in fan:
                    line = line.decode('utf-8')
                    data = line.split("\t")
                    print(str(len(data)))
                    if len(data)>1:
                        stemmed_tokens = stemmed_tokens + " " + data[2]

            stemmed_line = parts[0]+"\t"+stemmed_tokens+"\t"+parts[2]
            with open(filename_stemmed,'ab') as ftrain:
                ftrain.write(stemmed_line.encode("utf-8"))


# execute only if run as a script
if __name__ == "__main__":
    main()