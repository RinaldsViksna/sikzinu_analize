import sys
import os
import json
import time
import re

# argv[1] - filename to process
# processed file is saved in the same dir as source

def main():
    filename = os.path.splitext(sys.argv[1])[0]
    filename_to_save = filename + "_ustali.tsv"
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
            # replace links from tweetText
            tweetText = re.sub(r'http(.*?)(\s|$)','_link ',tweetText)
            # replace usernames from tweetText
            tweetText = re.sub(r'@(.*?)(\s|$)','_user ',tweetText)
            # replace hashtags from tweetText
            tweetText = re.sub(r'#(.*?)(\s|$)','_tag ',tweetText)

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