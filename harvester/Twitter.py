import tweepy
import json
import re
import couchdb
from nltk.corpus import wordnet_ic
import nltk
from profanity import profanity
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from tweepy.streaming import StreamListener
from tweepy import Stream

#lin-similarity is caculated based on the brown.dat

nltk.download('wordnet_ic')
brown_info_content = wordnet_ic.ic('ic-brown.dat')

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

# analyze sentiment. input is string,return a dictionary including positive probability.

#negative probability and when positive int, positive, negtive int ,negative. zero, neutual

def sentiment_analysis(content):

    sentiAnalyzer = SentimentIntensityAnalyzer()
    return sentiAnalyzer.polarity_scores(content)



# check if the sentence have a profanity word.
def profanity_analysis(content):
    containProfanity = profanity.contains_profanity(content)
    return containProfanity



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

    word_a = lemmatizer.lemmatize(word, 'a')
    for synset in wn.synsets(word_a, 'a'):
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

    word_a = lemmatizer.lemmatize(word, 'a')
    for synset in wn.synsets(word_a, 'a'):
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

        tweetdata = json.loads(data.encode('utf-8'))
        tweetdata = add_id(tweetdata)

        tweetReal = removehttp(tweetdata)
        contentText1 = re.sub(r'#(\w+)\b', ' $1 ', tweetReal)
        contentText = re.sub(r'@\w+\b', '', contentText1)

        tweetid = tweetdata['id']
        print(tweetid)


        sentiment = sentiment_analysis(contentText)
        try:
            profanity = profanity_analysis(contentText)
        except:
            profanity = False
        crime = crime_analysis(contentText)
        wrath = wrath_analysis(contentText)
        lust = lust_analysis(contentText)

        # Update
        tweetdata['sentiment'] = sentiment
        tweetdata['profanity'] = profanity
        if sentiment["compound"] < -0.5 and crime:
            tweetdata['crime'] = crime
        elif not crime:
            tweetdata['crime'] = crime
        else:
            tweetdata['crime'] = not crime

        if sentiment["neg"] > 0 and wrath:
            tweetdata['wrath'] = wrath
        elif not wrath:
            tweetdata['wrath'] = wrath
        else:
            tweetdata['wrath'] = not wrath

        if sentiment["neg"] > 0.2 and lust:
            tweetdata['lust'] = lust
        elif not lust:
            tweetdata['lust'] = lust
        else:
            tweetdata['lust'] = not lust



        tweetsave = json.dumps(tweetdata)
        self.savetodb(tweetsave)
        return True

    def on_status(self, status):
        print(status.text)

    def on_error(self, status):
        print(status)

    def savetodb(self, data):
        address = "http://127.0.0.1:5984/" #just change the address to save the DB
        couch = couchdb.Server(address)
        try:
            db = couch.create('geotry') # create db table
        except:
            db = couch['geotry']

        try:
            db.save(json.loads(data.encode('utf-8')))
        except:
            pass


def main():

    #This handles Twitter authetification and the connection to Twitter Streaming API
    try:
        listener = tweetListener()
        stream = Stream(getKeyToken(), listener)

    # Only search tweets in restricted area and default language is English
        stream.filter(languages=["en"], locations = [113.338953078, -43.6345972634, 153.569469029, -10.6681857235])
    except Exception as e:
        print(e)
        time.sleep(60)

main()
