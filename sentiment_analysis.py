from textblob import TextBlob as tb
import tweepy
import numpy as np

from pymongo import MongoClient
client = MongoClient("mongodb+srv://wesleyeduardocr7:Wesd8123@cluster0-joqds.mongodb.net/test?retryWrites=true&w=majority")
#client = MongoClient('localhost',27017)

db = client.get_database('sentiment_analysis')

consumer_key = '8sqJYjU0Z3GSQjzY76Y3cEK5d'
consumer_secret = 'ZzpEW2htXlxoY8pOOwmzl1irwAz1d6iguf4bh8YzBhwZEIOD6t'
access_token = '1045828227015618560-U3JneyClKT3Hh2cLcSs9Psg60yoXGa'
access_token_secret = 'u2Mw3urs5CVXnlv8VkSGDDx8IHZ0ByHTIfUeyrlrN87ZQ'

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


    