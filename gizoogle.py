import requests
import re
import twitter
from bs4 import BeautifulSoup
import json
import os
from twitkeys import TWITTER_KEY, TWITTER_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


TWITTER_HANDLES = ['@realDonaldTrump', '@POTUS']
HASHTAG = ' #Trizump'

def main():
    tweeted = load_tweets()        
    api = twitter_api()
    tweets = get_tweets(api)
    send_tweets(tweets, tweeted, api)           
    save_tweets(tweeted)


def send_tweets(tweets, tweeted, api):
    for tweet in reversed(tweets):
        
        if tweet.id_str not in tweeted['tweets']:
        
            twizeet = gizoogle(tweet.text) + HASHTAG
            print('going to tweet id# {}'.format(tweet.id_str))

            try:
                if len(twizeet) > 274:
                    splits = twizeet.split()
                    twizeet1 = ' '.join(splits[:int(len(splits)/3)]) + '..'
                    twizeet2 = '..' + ' '.join(splits[int(len(splits)/3):int(len(splits)*2/3)]) + '..'
                    twizeet3 = '..' + ' '.join(splits[int(len(splits)*2/3):])
                    api.PostUpdate(twizeet1)
                    api.PostUpdate(twizeet2)
                    api.PostUpdate(twizeet3)
                    tweeted['tweets'].append(tweet.id_str)

                elif len(twizeet) > 140:
                    splits = twizeet.split()
                    twizeet1 = ' '.join(splits[:int(len(splits)/2)]) + '..'
                    twizeet2 = '..' + ' '.join(splits[int(len(splits)/2):])
                    api.PostUpdate(twizeet1)
                    api.PostUpdate(twizeet2)
                    tweeted['tweets'].append(tweet.id_str)

                else:
                    api.PostUpdate(twizeet)
                    tweeted['tweets'].append(tweet.id_str)

            except Exception as e:
                print(e)

        else:
            print('{} already tweeted.'.format(tweet.id_str))


def get_tweets(api):

    tweets = []
    tweet_text = []

    for handle in TWITTER_HANDLES:
        tweets = api.GetUserTimeline(screen_name=handle)
        for tweet in tweets:
            if tweet.text not in tweet_text:
                tweets.append(tweet)
                tweet_text.append(tweet.text)
                
    return tweets


def gizoogle(text):
    data = {'translatetext':text}
    r = requests.post('http://www.gizoogle.net/textilizer.php', data=data)
    soup = BeautifulSoup(r.text, 'html.parser')
    gizoogled = soup.form.get_text()

    print('****************')
    print('CONVERTED{}\n\nINTO\n{}'.format(text, gizoogled))
    print('****************')

    return gizoogled


def twitter_api():
    api = twitter.Api(consumer_key=TWITTER_KEY,
                      consumer_secret=TWITTER_SECRET_KEY,
                      access_token_key=ACCESS_TOKEN,
                      access_token_secret=ACCESS_TOKEN_SECRET)
    return api


def load_tweets():
    base_folder = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(base_folder, 'tweeted.json')
    if os.path.isfile(path):
        with open(path) as filein:
            tweeted = json.load(filein)
    else:
        tweeted = {'tweets': []}
    return tweeted


def save_tweets(tweeted):
    base_folder = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(base_folder, 'tweeted.json')
    with open(path, 'w') as outfile:
        json.dump(tweeted, outfile)

    
if __name__ == '__main__':
    main()
