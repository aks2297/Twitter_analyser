import tweepy
import numpy as np 
import pandas as pd
import argparse
import time
from tweepy.auth import OAuthHandler
from textblob import TextBlob
import sys
reload(sys)
sys.setdefaultencoding('utf8')
parser = argparse.ArgumentParser()
parser.add_argument('--search_tw', type=str, help='Enter the string to be searched')
parser.add_argument('--max', type=int, help='Maximum number of tweets in the CSV file')
args = parser.parse_args()
max_size=args.max
search = args.search_tw  
#replace the '&' in the following variables with your own keys and tokens
consumer_key='&&&&'
consumer_secret='&&&&'

access_token='&&&&&'
access_token_secret='&&&&'

auth=OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
count=1 
#to keep a count of how many tweets are being executed 
arr=np.array(['Statement', 'Senti_val'])
api=tweepy.API(auth)
class SentiCalc(tweepy.StreamListener):
    def on_status(self, status):
        global count, arr
        analysis = TextBlob(status.text) 
        #analysis of tweetss
        if analysis.sentiment.polarity > 0.3:
            Sent = 'Positive'
        elif analysis.sentiment.polarity < 0.3:
            Sent = 'Negative'
        else:
            Sent =	'Neutral'
            
        tw = (status.text).encode('utf-8')
        #encoding of tweets to understandable format(we can use djangoUtils class too
        if '@' in tw:
            tw = tw.split(':') 
            if len(tw) > 1:
                arr = np.vstack([arr, [tw[1], Sent]]) 
     

        if count > max_size:
            df = pd.DataFrame(arr[1:], columns=[arr[0]]) 
            df.to_csv('{}.csv'.format(search))  
            exit()
SentiCalc=SentiCalc()
myStream = tweepy.Stream(auth=api.auth, listener=SentiCalc, languages=["en"]) 
myStream.filter(track=['{}'.format(search)])
#streaming of the tweets with the name you entered in search_tw
