import jsonify
import Queue
import time

import tweepy

from auth import consumer_key, consumer_secret, access_token, access_token_secret

string_to_search = 'RT to win enter'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

following = Queue.Queue()
following_count = 0

past_tweet_ids = []

while True:
    tweets = api.search(string_to_search)
    tweet_id_dict = {tweet.id : tweet for tweet in tweets if tweet.id not in past_tweet_ids}
    for tweet_id in tweet_id_dict.keys():
        print 'Retweeting ' + str(tweet_id)
        api.retweet(tweet_id)
        if 'follow' in tweet_id_dict.get(tweet_id).text:
            user_id_to_follow = jsonify(tweet_id_dict.get(tweet_id)._json)['id_str']
            api.create_friendship(user_id_to_follow, True)
            if following_count > 1500:
                user_id_to_unfollow = following.get()
                api.destroy_friendship(user_id_to_unfollow)
                following_count = following_count - 1
            following.put(user_id_to_follow)
            following_count = following_count + 1
        time.sleep(60)
    past_tweet_ids = past_tweet_ids + tweet_id_dict.keys()