# -*- coding: utf-8 -*-

# import modules
import tweepy
import time

# import dependencies
from config import *

# authorize twitter app
def init():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api
    
def main():
    api = init()
    
    # start if 06.00 UTC + 3
    while True:
        # lookup for tweets
        # check for errors
        tweets = lookup()
        
        # update twitter's account status
        for tweet in tweets:
            #check for errors
            api.update_status(tweet)
        
        # delay next tweet for 3 hours
        time.sleep(10800000)

if __name__ == "__main__":
    main()