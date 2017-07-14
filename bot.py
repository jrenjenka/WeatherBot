#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import modules
import tweepy
import time

# import dependencies
from config import *

# authorize twitter app
def init():
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)
    except tweepy.TweepError:
        raise RuntimeError("ERROR: cannot authorize the app") from None
    
def main():
    try:
        api = init()
    except ValueError:
        raise RuntimeError("ERROR: authorization failed") from None
    
    while True:
        # lookup for tweets
        try:
            tweets = ["test1", "test2", "test3"]
            # update twitter's account status
            for tweet in tweets:
                #check for errors
                api.update_status(tweet)
        except ValueError:
            print("ERROR: cannot get weather data")
        
        # delay next tweet for 3 hours
        # time.sleep(10800000)

if __name__ == "__main__":
    main()