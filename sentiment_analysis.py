from textblob import TextBlob as tb
import tweepy
import numpy as np

from pymongo import MongoClient
client = MongoClient("")
#client = MongoClient('localhost',27017)

db = client.get_database('sentiment_analysis')

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

public_tweets = api.search('Maranhão')

for tweet in public_tweets:   
    
    analysis = tb(tweet.text)
    
    polarity = analysis.sentiment.polarity
    
    db.tweets.insert_one({        
        "tweet": tweet.text,
        "polarity": polarity
    })


    