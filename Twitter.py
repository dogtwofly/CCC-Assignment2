import tweepy
import json
import re
import couchdb

import nltk
from profanity import profanity
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# My keys and tokens
consumer_key = 'UjnHPModDzohpESefLeSCncAk'
consumer_secret = '2OWQ9zYinzMZB3gUQx3o3tfIdt0JX2x00hRoBJqcxBN9I5E4nv'
access_token = '988327751126925312-ts0LnQL22Cb1IOPnrHyobyu6BVWjTsO'
access_token_secret = '9aRnHHOcLwVsHfw2264JebZQExWZKAZAxW2b6eOKGLF5D'

# Get the authentication
def getKeyToken():

    access = {"consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "access_token": access_token,
            "access_secret": access_token_secret}

    auth = tweepy.OAuthHandler(access['consumer_key'], access['consumer_secret'])
    auth.set_access_token(access['access_token'], access['access_secret'])
    return auth




# analyze sentiment. input is string,return a dictionary including pos: postive probability.

#neg: negative probability. compoud: when positive int, positive, negtive int ,negative. zero, neutual

def sentiment_analysis(content):

    senti_analyzer=SentimentIntensityAnalyzer()
    return senti_analyzer.polarity_scores(content)



# check if the sentence have a profanity word.
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


def add_id(tweetdata):
    id=tweetdata['id']
    tweetdata['_id']=str(id)
    return tweetdata


# Tweet listener
class tweetListener(StreamListener):

    def on_data(self, data):

        tweetdata = json.loads(data.encode('gbk'))
        tweetdata = add_id(tweetdata)

        tweetReal = removehttp(tweetdata)
        #print (tweetReal)

        tweetid = tweetdata['id']
        print (tweetid)
        # Call analysis functions
        sentiment = sentiment_analysis(tweetReal)
        profanity = profanity_analysis(tweetReal)
        crime = crime_analysis(tweetReal)


        # Print
        print (sentiment)
        print (profanity)
        print (crime)


        # Update
        tweetdata['sentiment'] = sentiment
        tweetdata['profanity'] = profanity
        tweetdata['crime'] = crime


        tweetsave = json.dumps(tweetdata)
        self.savetodb(tweetsave)


        return True

    def on_status(self, status):
        print(status.text)

    def on_error(self, status):
        print (status)

    def savetodb(self, data):
        address = "http://127.0.0.1:5984/" #just change the address to save the DB
        couch = couchdb.Server(address)
        try:
            db = couch.create('truetweet') # create db table
        except:
            db = couch['truetweet']

        try:
            db.save(json.loads(data.encode('utf-8')))
        except:
            pass


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API

    listener = tweetListener()
    stream = Stream(getKeyToken(), listener)

    # Only search tweets in restricted area
    stream.filter(locations = [144, -38, 145, -37])

tweepy.close()
