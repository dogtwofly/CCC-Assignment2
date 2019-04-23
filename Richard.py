import requests
import couchdb
import json

import re
import nltk
from profanity import profanity
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from requests.auth import HTTPDigestAuth


# Delete Origin '_id' & '_rev'
def add_id(tweetdata):
    del saveitem['_rev']
    del tweetdata['_id']
    id = tweetdata['id_str']
    tweetdata['_id'] = id
    return tweetdata


# Sentiment Analysis
def sentiment_analysis(content):
    senti_analyzer=SentimentIntensityAnalyzer()
    return senti_analyzer.polarity_scores(content)


def profanity_analysis(content):
    content=re.sub(r'#(\w+)\b',' $1 ',content)
    content=re.sub(r'@\w+\b','',content)
    contain_profanity=profanity.contains_profanity(content)

    return contain_profanity


# check if the word is relevant to crime
def check_crime(word):
    max=0
    lemmatizer = WordNetLemmatizer()
    word_n = lemmatizer.lemmatize(word, 'n')

    for synset in wn.synsets(word_n,'n'):
        if max<synset.wup_similarity(wn.synset("crime.n.01")):
            max=synset.wup_similarity(wn.synset("crime.n.01"))

        if max<synset.wup_similarity(wn.synset("crime.n.02")):
            max=synset.wup_similarity(wn.synset("crime.n.02"))

        if max<synset.wup_similarity(wn.synset("assault.n.01")):
            max=synset.wup_similarity(wn.synset("assault.n.01"))

        if max<synset.wup_similarity(wn.synset("robbery.n.01")):
            max=synset.wup_similarity(wn.synset("robbery.n.01"))

        if max<synset.wup_similarity(wn.synset("fraud.n.01")):
            max=synset.wup_similarity(wn.synset("fraud.n.01"))

        if max<synset.wup_similarity(wn.synset("arson.n.01")):
            max=synset.wup_similarity(wn.synset("arson.n.01"))

        if max<synset.wup_similarity(wn.synset("extortion.n.01")):
            max=synset.wup_similarity(wn.synset("extortion.n.01"))

        if max<synset.wup_similarity(wn.synset("larceny.n.01")):
            max=synset.wup_similarity(wn.synset("larceny.n.01"))

    word_v = lemmatizer.lemmatize(word, 'v')

    for synset in wn.synsets(word_v, 'v'):
        if max < synset.wup_similarity(wn.synset("rob.v.01")):
            max = synset.wup_similarity(wn.synset("rob.v.01"))

        if max<synset.wup_similarity(wn.synset("assault.v.01")):
            max=synset.wup_similarity(wn.synset("assault.v.01"))

        if max<synset.wup_similarity(wn.synset("rob.v.01")):
            max=synset.wup_similarity(wn.synset("rob.v.01"))

        if max<synset.wup_similarity(wn.synset("extort.v.01")):
            max=synset.wup_similarity(wn.synset("extort.v.01"))

        if max<synset.wup_similarity(wn.synset("murder.v.01")):
            max=synset.wup_similarity(wn.synset("murder.v.01"))

    return max


def crime_analysis(content):
    content = re.sub(r'#(\w+)\b', ' $1 ', content)
    content = re.sub(r'@\w+\b', '', content)
    tokens = nltk.word_tokenize(content.lower())

    max=0.0

    for token in tokens:
        if max<check_crime(token):
            max=check_crime(token)

    if max>0.8:
        return True
    else:
        return False

# Remove "http" information in tweet text
def removehttp (tweetdata):

    try:
        text = tweetdata['extended_tweet']['full_text']
    except:
        text = tweetdata['text']

    pattern = re.compile('https://t.co/\w+')
    pat = pattern.findall(text)
    if len(pat) is 1:
        aa = pat[0]
        text = text.replace(aa, "")

    return text


# Save to couchdb
def savetodb(data):
    address = "http://127.0.0.1:5984/" #just change the address to save the DB
    couch = couchdb.Server(address)

    try:
        db = couch.create('newtweet') # create db table
    except:
        db = couch['newtweet']  #

    try:
        db.save(data)
    except:
        pass




# Get Message
url='http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/geoindex'
para={'include_docs':'true','reduce':'false','skip':'0','limit':'100'}

offset = 100
current = 0

while (current < 1000000):


    message=requests.get(url,para,auth=('readonly', 'ween7ighai9gahR6'))


    current = current + offset
    temp = current
    para['skip'] = str(temp)

    dataset = message.json() # Message to dict
    tweets = dataset['rows'] # List of tweets
    print ("Done! "+ str(current) + "Tweets")


    for tweet in tweets:
        saveitem = tweet['doc']

        id = saveitem['id_str']
        content = saveitem['text']
        # print(id)
        saveitem = add_id(saveitem)
        tweetReal = removehttp(saveitem)
        # print (tweetReal)


        # Call analysis functions
        sentiment = sentiment_analysis(tweetReal)
        try:
            profanity = profanity_analysis(tweetReal)
        except:
            profanity = False
        crime = crime_analysis(tweetReal)


        # Update
        saveitem['sentiment'] = sentiment
        saveitem['profanity'] = profanity
        saveitem['crime'] = crime

        tweetsave = json.dumps(saveitem)


        savetodb(saveitem)

