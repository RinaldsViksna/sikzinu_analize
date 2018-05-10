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

def main():
    filename = os.path.splitext(sys.argv[1])[0]
    filename_clean = filename + "_emojis.tsv"
    try:
        os.remove(filename_clean)
    except OSError:
        pass

    emojis = {}
    with open ('emoji.tsv','rb') as stopWordsFile:
        for line in stopWordsFile:
            line = line.decode('utf-8-sig')
            emoji = line.split("\t")
            emojis[emoji[0]] = emoji[1]

    with open(sys.argv[1],'rb') as f:
        for line in f:
            line = line.decode('utf-8')
            parts = line.split("\t")
            tweetText = parts[1]

            # replace links from tweetText to avoid https:/ giving negative emoji
            tweetText = re.sub(r'http(.*?)(\s|$)','_link ',tweetText)
            cleanText = ""

            for key,value in emojis.items():
                tweetText = tweetText.replace(key," "+value.strip()+" ")
            cleanText = tweetText

            clean_line = parts[0]+"\t"+cleanText+"\t"+parts[2]
            with open(filename_clean,'ab') as fout:
                fout.write(clean_line.encode("utf-8"))


# execute only if run as a script
if __name__ == "__main__":
    main()