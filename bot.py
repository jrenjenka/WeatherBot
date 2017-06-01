# import modules
import tweepy

# import dependencies
from config import *

# authorize twitter application
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
