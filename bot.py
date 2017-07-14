#!/usr/bin/env python3
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
    return tweepy.API(auth)
   
def main():
    api = init()
    
    while True:
        # lookup for tweets
        #tweets = lookup()
        tweets = ["test4", "test5"]
        
        # update twitter's account status
        for tweet in tweets:
            try: api.update_status(tweet)
            except tweepy.TweepError: print("ERROR: cannot get weather data")
        
        # delay next tweet for 3 hours
        time.sleep(10800000)

if __name__ == "__main__":
    main()