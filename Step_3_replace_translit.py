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
# processed file is saved in the same dir as source as filename_replace_translit.tsv

def main():
    filename = os.path.splitext(sys.argv[1])[0]
    filename_clean = filename + "_translit.tsv"
    try:
        os.remove(filename_clean)
    except OSError:
        pass

    translitRules = {}
    with open ('translit_rules.tsv','rb') as translitRulesFile:
        for line in translitRulesFile:
            line = line.decode('utf-8-sig')
            translitRule = line.split("\t")
            translitRules[translitRule[0]] = translitRule[1]

    with open(sys.argv[1],'rb') as f:
        for line in f:
            line = line.decode('utf-8')
            parts = line.split("\t")
            tweetText = parts[1]
            cleanText = ""

            for key,value in translitRules.items():
                tweetText = tweetText.replace(key,value.strip())
            cleanText = tweetText

            clean_line = parts[0]+"\t"+cleanText+"\t"+parts[2]
            with open(filename_clean,'ab') as fout:
                fout.write(clean_line.encode("utf-8"))


# execute only if run as a script
if __name__ == "__main__":
    main()