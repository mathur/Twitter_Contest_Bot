import Queue
import time

import tweepy

from auth import consumer_key, consumer_secret, access_token, access_token_secret

string_to_search = 'RT retweet to win'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

following = Queue.Queue()
following_count = 0

past_tweet_ids = []

blacklisted_users = [3044534229]

while True:
    tweets = api.search(string_to_search)
    tweet_id_dict = {tweet.id : tweet for tweet in tweets if tweet.id not in past_tweet_ids}
    for tweet_id in tweet_id_dict.keys():
        try:
            api.retweet(tweet_id)
            print 'Retweeted ' + str(tweet_id)
            user_id_to_follow = tweet_id_dict.get(tweet_id).retweeted_status.user.id
            if user_id_to_follow not in blacklisted_users:
                if 'follow' in tweet_id_dict.get(tweet_id).text.lower():
                    api.create_friendship(user_id_to_follow, True)
                    print 'Followed ' + str(user_id_to_follow)
                    if following_count > 1500:
                        user_id_to_unfollow = following.get()
                        api.destroy_friendship(user_id_to_unfollow)
                        following_count = following_count - 1
                    following.put(user_id_to_follow)
                    following_count = following_count + 1
            else:
                print 'Blacklisted user. Continuing onwards.'
        except tweepy.error.TweepError, e:
            error_code = list(e)[0][0].get('code')
            if error_code == 327:
                print 'Already retweeted, moving on'
            elif error_code == 88:
                print 'Rate limit exceeded, waiting 16 minutes!'
                time.sleep(15 * 60)
            elif error_code == 226:
                print 'Twitter thinks we are automating something. Stopping for a little bit'
                time.sleep(15 * 60)
            elif error_code == 261:
                # twitter disabled write for our application. fuck.
                # time to beautifulsoup up a new twitter app amirite
                print 'Twitter disabled the API key(s). Damn.'
            else:
                print str(e)
        except AttributeError:
            print 'Something went wrong. Moving on.'
        except Error, e:
            print str(e)
        time.sleep(30)
    past_tweet_ids = past_tweet_ids + tweet_id_dict.keys()