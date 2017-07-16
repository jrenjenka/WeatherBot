#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import modules
import tweepy
import time

# import dependencies
from config import *
from weather import *

# authorize twitter app
def init():
    """Authorize twitter app using tweepy library"""
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)
   
def main():
    """Run bot"""
    
    # initialize bot
    api = init()
    
    while True:
        # lookup for tweets
        tweets = lookup()
        
        # update twitter's account status
        if tweets != None:
            for tweet in tweets:
                api.update_status(tweet)
                
        # delay next tweet for 3 hours
        time.sleep(10800000)

if __name__ == "__main__":
    main()