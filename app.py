import time

import tweepy

from auth import consumer_key, consumer_secret, access_token, access_token_secret

string_to_search = 'RT to win'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

past_status_ids = set()

while True:
    tweets = api.search(string_to_search)
    tweet_id_list = set([tweet.id for tweet in tweets])
    new_tweet_ids = tweet_id_list - past_status_ids
    past_status_ids = tweet_id_list | past_status_ids

    for tweet_id in new_tweet_ids:
        print "Retweeting " + str(tweet_id)
        api.retweet(tweet_id)
        time.sleep(60)