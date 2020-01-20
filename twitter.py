import tweepy
from tweepy import OAuthHandler
from tweepy import StreamListener
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import pandas as pd



class TweetListner(StreamListener):
    def __init__(self, Fatched_tweets_filename):
        self.fatched_file_name = Fatched_tweets_filename
    
    def on_data(self, data):
        print(data)
        with open(self.fatched_file_name , 'a') as tweet_file:
            tweet_file.write(data)
        return True
    
    def on_error(self, status):
        print(status)

class TwitterAuthentication():
    def twitter_app_authenticate(self):
        consumer_key = '--------------------------'
        consumer_secret = '---------------------------'
        access_token = '----------------------------'
        access_token_secret = '------------------------'

        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth

class TweetStreamer():
    def __init__(self):
        self.twitter_authenticator = TwitterAuthentication()

    def stream_tweet(self, Fatched_tweets_filename, hash_tag_list):
        auth = self.twitter_authenticator.twitter_app_authenticate()
        listener = TweetListner(Fatched_tweets_filename)
        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list) 

class TwitterClient():
    def __init__(self, user_name=None):
        self.twitter_authenticator = TwitterAuthentication()
        self.auth = self.twitter_authenticator.twitter_app_authenticate()
        self.client = API(self.auth)
        self.twitter_user = user_name

    def get_user_timeline_tweet(self, num_tweet=10):        
        twits = Cursor(self.client.user_timeline, id=self.twitter_user).items(num_tweet)
        tweet =[]
        for tweets in twits:
            tweet.append(tweets)
        return tweet

class TweetAnalyze():

    def to_DataFrame(self, tweets):
        df = pd.DataFrame(data = [tw.text for tw in tweets], columns=['Tweet_text'])
        df['id'] = [tw.id for tw in tweets]
        df['Date'] = [tw.created_at for tw in tweets]
        df['user'] = [tw.user for tw in tweets]
        df['favorite_count'] = [tw.favorite_count for tw in tweets]
        df['retwwet'] = [tw.retweeted for tw in tweets]
        return df

class Tweet_to_csv():
    def __init__(self, FileNameCsv, tweets):
        self.tweetanalyze = TweetAnalyze()
        self.FileNameCsv = FileNameCsv
        self.tweets = tweets

    def to_csv(self):
        tweet_df = self.tweetanalyze.to_DataFrame(self.tweets)
        return tweet_df.to_csv(self.FileNameCsv,encoding='UTF=8')

if __name__ == "__main__":
    a = TwitterClient('Amit shah')
    tweet = a.get_user_timeline_tweet(num_tweet=200) 
    
    write = Tweet_to_csv(FileNameCsv= 'AmitShahTweet.csv', tweets=tweet)
    write.to_csv()

# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', 
# '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', 
# '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__',
#  '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
#   '_api', '_json', 'author', 'contributors', 'coordinates', 'created_at', 'destroy', 'entities', 'favorite',
#    'favorite_count', 'favorited', 'geo', 'id', 'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id',
#     'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'is_quote_status', 'lang',
#      'parse', 'parse_list', 'place', 'possibly_sensitive', 'quoted_status', 'quoted_status_id', 'quoted_status_id_str', 
#      'retweet', 'retweet_count', 'retweeted', 'retweets', 'source', 'source_url', 'text', 'truncated', 'user']
