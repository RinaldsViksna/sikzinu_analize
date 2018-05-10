import sys
import os
import json
import time
import re

# argv[1] - filename to process
# processed file is saved in the same dir as source

def main():
    filename = os.path.splitext(sys.argv[1])[0]
    filename_to_save = filename + "_num.tsv"
    try:
        os.remove(filename_to_save)
    except OSError:
        pass
    #print(filename)
    f = open(sys.argv[1],'rb')  
    lines = f.read().splitlines()
    for line in lines:
        line = line.decode('utf-8')
        #print(type(line))
        try: 
            tweet = line.split("\t")
            tweetText = tweet[1]
            # replace links from tweetText to avoid splitting links
            tweetText = re.sub(r'http(.*?)(\s|$)','_link ',tweetText)

            # remove punctuation from tweetText
            # tweetText = re.sub(r'[\.,\?\!:\(\)-;]+',' ',tweetText)
            tweetText = re.sub(r'[\.\,\?\!:\(\)\-\;\/\%\[\]\@\+\”\"\'#“«»/]+',' ',tweetText)
            # replace numbers from tweetText
            tweetText = re.sub(r'^\d+.\d+\s|\s\d+.\d+\s|\s\d+.\d+$',' _num ',tweetText)
            tweetText = re.sub(r'^\d+:\d+\s|\s\d+:\d+\s|\s\d+:\d+$',' _num ',tweetText)
            tweetText = re.sub(r'^\d+.\s|\s\d+.\s|\s\d+.$',' _num ',tweetText) 
            tweetText = re.sub(r'^\d+,\s|\s\d+,\s|\s\d+,$',' _num ',tweetText) 
            tweetText = re.sub(r'^\d+\s|\s\d+\s|\s\d+$',' _num ',tweetText) 
            
            
            # tweetText = re.sub(r'^\d+\s|\s\d+\s|\s\d+$','_num ',tweetText)

            processed_tweet = tweet[0]+"\t"+tweetText+"\t"+tweet[2]+"\n"
            with open(filename_to_save,'ab') as ftrain:
                ftrain.write(processed_tweet.encode("utf-8"))
                
        except Exception as e:
            print(e)
            print(type(line))
            print(line)
            time.sleep(33)
            pass

# execute only if run as a script
if __name__ == "__main__":
    main()