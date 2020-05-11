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
    print('3 - Busca Tweets por Parâmetro')  
    print('4 - Quantidade Total de Tweets')  
    print('5 - Inserir Frase Manual e Realizar Análise Sentimental')
    print('6 - Imprimir Frases com Polaridade')
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
    elif(op == 4):
      print('\n\nQuantidade Total de Tweets: ' + str(count_tweets())) 
      print('\n')
      main() 
    elif(op == 5):
      parameter = input("\nInforme a Frase: ")
      polarity_of_manually_inserted_phrases(parameter)
      main()
      print('\n')
    elif(op == 6):    
      print_polarity_phrases()
      main()    
    elif(op == 0):
      exit
    else:
        print('\nOpção Incorreta\n')
        main()
        


def insert_tweets(quant_loops, search_parameter):    

    count = 0

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

            count +=1

    print('Quantidade de Tweets Gerado: ' + str(count))


def print_polarity_tweets():

    for tweet in db.tweets.find():
        print('\n')   
        print('Parâmetro de Busca: ' +  str(tweet['parameter'])) 
        print('Tweet: ' +  str(tweet['tweet'])) 
        print('Nível do Sentimento: ' +  str(tweet['polarity']))
    
    print('\n\nQuantidade de Tweets: ' + str(count_tweets()))
   

def print_polarity_tweets_parameter(parameter):

    count = 0

    for tweet in db.tweets.find({"parameter": parameter }):
        print('\n')
        print('Tweet: ' +  str(tweet['tweet'])) 
        print('Nível do Sentimento: ' +  str(tweet['polarity']))
        count +=1
    
    print('\n\nQuantidade de Tweets: ' + str(count))

def count_tweets():

    count = 0

    for tweet in db.tweets.find():
        count +=1

    return count

def polarity_of_manually_inserted_phrases(parameter):

   analysis = tb(parameter)
    
   polarity = analysis.sentiment.polarity

   db.phrases.insert_one({  
                "phrase": parameter,                
                "polarity" : polarity
            })

   print('\n')
   print('Frase: ' +  str(parameter)) 
   print('Nível do Sentimento: ' +  str(polarity))
   print('\n')

def print_polarity_phrases():

    for phrase in db.phrases.find():
        print('\n')        
        print('Frase: ' +  str(phrase['phrase'])) 
        print('Nível do Sentimento: ' +  str(phrase['polarity']))
    
    print('\n\nQuantidade de Frases: ' + str(count_phrases()))

    print('\n')

def count_phrases():

    count = 0

    for phrase in db.phrases.find():
        count +=1

    return count

main()