import requests
import couchdb
import json
from nltk.corpus import wordnet_ic

import re
import nltk
from profanity import profanity
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

nltk.download('wordnet_ic')
brown_info_content = wordnet_ic.ic('ic-brown.dat')
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
    print("______________________________________")
    print("This is test"+str(content))
    print("______________________________________")
    contain_profanity=profanity.contains_profanity(content)

    return contain_profanity


# check if the word is relevant to crime
def check_crime(word):
    max=0
    lemmatizer = WordNetLemmatizer()
    word_n = lemmatizer.lemmatize(word, 'n')

    for synset in wn.synsets(word_n,'n'):
        listnoun = ["crime.n.01", "crime.n.02", "assault.n.01", "robbery.n.01", "fraud.n.01", "arson.n.01", "extortion.n.01", "larceny.n.01", "gun.n.01", "weapon.n.01", "blackmail.n.01"]
        for i in listnoun:
            if max<synset.lin_similarity(wn.synset(i), brown_info_content):
                max=synset.lin_similarity(wn.synset(i), brown_info_content)

    word_v = lemmatizer.lemmatize(word, 'v')

    for synset in wn.synsets(word_v, 'v'):
        listverb = ["rob.v.01", "assault.v.01", "extort.v.01", "murder.v.01", "kidnap.v.01", "blackmail.v.01"]
        for i in listverb:
            if max<synset.lin_similarity(wn.synset(i), brown_info_content):
                max=synset.lin_similarity(wn.synset(i), brown_info_content)
    return max


def crime_analysis(content):
    tokens = nltk.word_tokenize(content.lower())

    max=0.0

    for token in tokens:
        if max<check_crime(token):
            max=check_crime(token)

    if max>0.8:
        return True
    else:
        return False
# check if the word is relevant to wrath
def check_wrath(word):
    max = 0
    lemmatizer = WordNetLemmatizer()
    word_n = lemmatizer.lemmatize(word, 'n')
    for synset in wn.synsets(word_n,'n'):
        listnoun = ["outrage.n.01", "madness.n.01", "rage.n.01"]
        for i in listnoun:
            if max<synset.lin_similarity(wn.synset(i), brown_info_content):
                max=synset.lin_similarity(wn.synset(i), brown_info_content)

    word_v = lemmatizer.lemmatize(word, 'v')

    for synset in wn.synsets(word_v, 'v'):
        listverb = ["rage.v.01", "hate.v.01"]
        for i in listverb:
            if max < synset.lin_similarity(wn.synset(i), brown_info_content):
                max = synset.lin_similarity(wn.synset(i), brown_info_content)
    return max

    word_a = lemmatizer.lemmatize(word, 'v')
    for synset in wn.synsets(word_a, 'v'):
        listadjective = ["angry.a.01", "mad.a.01", "unhappy.a.01"]
        for i in listadjective:
            if max < synset.lin_similarity(wn.synset(i), brown_info_content):
                max = synset.lin_similarity(wn.synset(i), brown_info_content)
    return max

def wrath_analysis(content):
    tokens = nltk.word_tokenize(content.lower())

    max = 0.0

    for token in tokens:
        if max < check_wrath(token):
            max = check_wrath(token)

    if max > 0.8:
        return True
    else:
        return False
# check if the word is relevant to lust
def check_lust(word):
    max = 0
    lemmatizer = WordNetLemmatizer()
    word_n = lemmatizer.lemmatize(word, 'n')
    for synset in wn.synsets(word_n, 'n'):
        listnoun = ["sex.n.01", "sex.n.02", "love.n.01", "love.n.02"]
        for i in listnoun:
            if max < synset.lin_similarity(wn.synset(i), brown_info_content):
                max = synset.lin_similarity(wn.synset(i), brown_info_content)

    word_v = lemmatizer.lemmatize(word, 'v')

    for synset in wn.synsets(word_v, 'v'):
        listverb = ["desire.v.01", "want.v.01", "love.v.01", "love.v.02"]
        for i in listverb:
            if max < synset.lin_similarity(wn.synset(i), brown_info_content):
                max = synset.lin_similarity(wn.synset(i), brown_info_content)
    return max

    word_a = lemmatizer.lemmatize(word, 'v')
    for synset in wn.synsets(word_a, 'v'):
        listadjective = ["sexual.a.01", "sexual.a.02", "sexy.a.01", "sexy.a.02", "jealous.a.01", "jealous.a.02"]
        for i in listadjective:
            if max < synset.lin_similarity(wn.synset(i), brown_info_content):
                max = synset.lin_similarity(wn.synset(i), brown_info_content)
    return max

def lust_analysis(content):
    tokens = nltk.word_tokenize(content.lower())

    max = 0.0

    for token in tokens:
        if max < check_lust(token):
            max = check_lust(token)

    if max > 0.8:
        return True
    else:
        return False


# Remove "http" information in tweet text
def removehttp (tweet):

    try:
        text = tweet['extended_tweet']['full_text']
    except:
        text = tweet['text']

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
url='http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary'
para={'include_docs':'true','reduce':'false','skip':'0','limit':'100'} #'start_key':'["perth", 2018, 1, 1]', 'end_key':'["perth", 2018, 12, 31]'}

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
        contentText1 = re.sub(r'#(\w+)\b', ' $1 ', tweetReal)
        contentText = re.sub(r'@\w+\b', '', contentText1)

        # Call analysis functions
        sentiment = sentiment_analysis(contentText)
        try:
            profanity = profanity_analysis(contentText)
        except:
            profanity = False
        crime = crime_analysis(contentText)
        wrath = wrath_analysis(contentText)
        lust = lust_analysis(contentText)


        # Update
        saveitem['sentiment'] = sentiment
        saveitem['profanity'] = profanity
        if sentiment["compound"]<-0.5 and crime:
            saveitem['crime'] = crime
        elif not crime:
            saveitem['crime'] = crime

        if sentiment["neg"]>0 and wrath:
            saveitem['wrath'] = wrath
        elif not wrath:
            saveitem['wrath'] = wrath

        if sentiment["neg"]>0.2 and lust:
            saveitem['lust'] = lust
        elif not lust:
            saveitem['lust'] = lust


        tweetsave = json.dumps(saveitem)
        print(tweetsave)

        # savetodb(saveitem)

