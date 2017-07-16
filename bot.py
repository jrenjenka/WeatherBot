#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import modules
import tweepy
import time
import os

# import dependencies
from weather import *

# authorize twitter app
def init():
    """Authorize twitter app using tweepy library"""
    
    # ensure environment variables are set
    if not os.environ.get("consumer_key"):
        raise RuntimeError("consumer_key not set")
    if not os.environ.get("consumer_secret"):
        raise RuntimeError("consumer_secret not set")
    
    auth = tweepy.OAuthHandler(os.environ.get("consumer_key"), os.environ.get("consumer_secret"))
    auth.set_access_token(os.environ.get("access_token"), os.environ.get("access_token_secret"))
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