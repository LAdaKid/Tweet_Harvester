"""
Lee Alessandrini
Text Mining

Sources:

TextBlob Tutorial:
https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/

Flask Tweet Webapp Tutorial:
https://thelaziestprogrammer.com/sharrington/web-development/tweet-archiver-with-flask-and-tweepy-part-1
"""

from flask import Flask, json, request, render_template
import tweepy
import re
from textblob import TextBlob

app = Flask(__name__)
# Load our config from an object, or module (config.py)
app.config.from_object('config')

# These config variables come from 'config.py'
auth = tweepy.OAuthHandler(app.config['TWITTER_CONSUMER_KEY'],
                           app.config['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(app.config['TWITTER_ACCESS_TOKEN'],
                      app.config['TWITTER_ACCESS_TOKEN_SECRET'])
tweepy_api = tweepy.API(auth)

@app.route('/')
def hello_world():
    return "<h1>Hello World</h1>"


def get_tweets_for_username(username):
    tweets = tweepy_api.user_timeline(screen_name=username)
    return get_tweets(tweets)

def get_tweets_for_ticker(ticker):
    tweets = tweepy_api.search(q='$' + ticker, count=20)
    return get_tweets(tweets)

def get_tweets(tweets):
    tweet_list = []

    for t in tweets:
        print(t)
        tweet_list.append(
            {'tweet': t.text,
             'create_at': t.created_at,
             'username': t.user.name,
             'headshot_url': t.user.profile_image_url,
             'sentiment': get_tweet_sentiment(t.text)})

    return tweet_list

def get_tweet_sentiment(tweet): 
    ''' 
    Utility function to classify sentiment of passed tweet 
    using textblob's sentiment method 
    '''
    # create TextBlob object of passed tweet text 
    analysis = TextBlob(clean_tweet(tweet))

    # set sentiment 
    if analysis.sentiment.polarity > 0: 
        # For positive return 'success' for bootstrap green text
        return 'success'
    elif analysis.sentiment.polarity == 0:
        # For neutral return 'secondary' for bootstrap dark blue
        return 'secondary'
    else: 
        # For negative return 'danger' for bootstrap red
        return 'danger'


def clean_tweet(tweet): 
    ''' 
    Utility function to clean tweet text by removing links, special characters 
    using simple regex statements. 
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 


@app.route('/tweet-harvester/<string:username>')
def tweets(username):
  # 'tweets' is passed as a keyword-arg (**kwargs)
  # **kwargs are bound to the 'tweets.html' Jinja Template context
  return render_template("tweets.html", tweets=get_tweets_for_username(username))

@app.route('/tweet-harvester/ticker/<string:ticker_symbol>')
def ticker(ticker_symbol):
    return render_template("tweets.html", tweets=get_tweets_for_ticker(ticker_symbol))
