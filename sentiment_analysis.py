from textblob import TextBlob as tb
import tweepy
import numpy as np

from pymongo import MongoClient
client = MongoClient("")

db = client.get_database('sentiment_analysis')

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def main():
  
    print('1 - Extrair Tweets e Realizar Análise Sentimental')   
    print('2 - Imprimir Tweets com Polaridade')   
    print('3 - Busca por Parâmetro')  
    print('0 - Sair')

    op = int(input('Informe a Opção: '))

    if(op == 1):
        quant_loops = int(input('Quantidade de Loops:'))
        parameter = input("Informe a Palavra: ")
        insert_tweets(quant_loops,parameter)
        print('Tweets extraídos com sucesso!\n')
        main()
    elif(op == 2):
       print_polarity_tweets()
       print('\n')
       main()
    elif(op == 3):
       parameter = input("Informe a Palavra: ")
       print_polarity_tweets_parameter(parameter)  
       print('\n')
       main() 
    else:
        main()


def insert_tweets(quant_loops, search_parameter):    

    public_tweets = api.search(search_parameter)

    for i in range(quant_loops):

        for tweet in public_tweets:   

            analysis = tb(tweet.text)
    
            polarity = analysis.sentiment.polarity
            
            db.tweets.insert_one({  
                "parameter": search_parameter, 
                "tweet": tweet.text,
                "polarity" : polarity
            })


def print_polarity_tweets():

    for tweet in db.tweets.find():
        print('\n')   
        print('Parâmetro de Busca: ' +  str(tweet['parameter'])) 
        print('Tweet: ' +  str(tweet['tweet'])) 
        print('Nível do Sentimento: ' +  str(tweet['polarity']))
   

def print_polarity_tweets_parameter(parameter):

    for tweet in db.tweets.find({"parameter": parameter }):
        print('\n')
        print('Tweet: ' +  str(tweet['tweet'])) 
        print('Nível do Sentimento: ' +  str(tweet['polarity']))


main()