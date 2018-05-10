import sys
import io
import os
import json
import time

# Read JSON and save it as delimited text file file  for further processing
# remplace tabs and newlines with ordinary spaces, as those are used for field separation
# argv[1] - filename to process
# processed file is saved in the same dir as source

def main():
    filename = os.path.splitext(sys.argv[1])[0]
    filename_to_save = filename + ".tsv"
    try:
        os.remove(filename_to_save)
    except OSError:
        pass
    #print(filename)

    #data = json.load(io.open(sys.argv[1],mode='r',encoding='utf-8'))
    data = json.load(open(sys.argv[1],mode='rb'))
    
    tweets = []
    get_all(data, "tweet_id", tweets)
    # tweets is list of dictionaries now
    # if not tweets:
    #     get_all(data,"id",tweets)
    # if not tweets:
    #     get_all(data,"external_tweet_id",tweets)
    # if not tweets:
    #     get_all(data,"id",tweets)

    bad_count = 0
    total_count = 0
    pos_count = 0
    neg_count = 0
    neu_count = 0
    scored2 = 0
    scored3 = 0
    scored4 = 0
    for json_line in tweets:
        # viksna: {"tweet_id": 865436793742782464, "text": "Dienas viedie v\u0101rdi: j\u0101, t\u0101 mums ir, t\u0101 mums ir! (Prezidents V\u0113jonis @900sekundes)", "POS": 0, "NEG": 0, "NEU": 0, "IMP": 0, "NOT_LV": 0}
        sentiment = "IMP" # Default value, "impossible to understand"
        score = 0

        if int(json_line["IMP"])>score:
            sentiment = "IMP"
            score = int(json_line["IMP"])
        if int(json_line["NOT_LV"])>score:
            sentiment = "IMP"
            score = int(json_line["IMP"])

        if int(json_line["POS"])>score: # if pos is equal to score, this tweet stays IMP
            sentiment = "POS"
            score = int(json_line["POS"])
        if int(json_line["NEG"])==score: # either NEG score is equal to pos score or IMP score, either way setiment is impossible to tell
            sentiment = "IMP"
        if int(json_line["NEG"])>score:
            sentiment = "NEG"
            score = int(json_line["NEG"])
        if int(json_line["NEU"])==score: # either NEU score is equal to pos score or IMP score, either way setiment is impossible to tell
            sentiment = "IMP"
        if int(json_line["NEU"])>score:
            sentiment = "NEU"
            score = int(json_line["NEU"])

        if sentiment == "IMP":
            # this tweet is useless 
            bad_count = bad_count + 1
            continue

        text = json_line["text"]
        text = text.replace('\n',' ')
        text = text.replace('\t',' ')

        tweet = str(json_line["tweet_id"])+"\t"+text
        if sentiment == "POS":
            pos_count = pos_count + 1
            tweet = tweet+"\tPOS"
        if sentiment == "NEG":
            neg_count = neg_count + 1
            tweet = tweet+"\tNEG"
        if sentiment == "NEU":
            neu_count = neu_count + 1
            tweet = tweet+"\tNEU"
        #with io.open(filename_to_save, 'a',encoding='utf-8') as fout:
        with open(filename_to_save, 'ab') as fout:
            if score > 3:
                scored4 = scored4 + 1 
            if score == 3:
                scored3 = scored3 + 1
            if score == 2:
                scored2 = scored2 + 1  
            tweet = tweet + "\n"
            fout.write(tweet.encode("utf-8"))

    total_count = pos_count + neg_count + neu_count
    print("total:"+str(total_count)+" pos:"+str(pos_count)+" neu:"+str(neu_count)+" neg:"+str(neg_count)+" bad:"+str(bad_count))
    print("scored4:"+str(scored4)+" scored3:"+str(scored3)+" scored2:"+str(scored2))
"""
    Parse json and save all tweets containing key into tweets list
"""
def get_all(json, key, tweets):
    if isinstance(json, dict):
        for k in json:
            #print(k+"\n")
            if k==key:
                #print("appended")
                # print(json)
                tweets.append(json)            
            elif isinstance(json[k],(dict,list)):
                get_all(json[k],key, tweets)
    elif isinstance(json, list):
        for item in json:
            if isinstance(item,(list,dict)):
                get_all(item,key, tweets)


# execute only if run as a script
if __name__ == "__main__":
    main()