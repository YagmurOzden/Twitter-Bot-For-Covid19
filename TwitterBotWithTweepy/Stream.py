from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import numpy as np
import pandas as pd
#this is where i put my CONSUMER_KEY etc.
import keys


# # # # # TWITTER CLIENT # # # # #
class TwitterClient():
    def __init__(self,twitter_user=None):
        self.auth=TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client=API(self.auth)
        self.twitter_user=twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    # How many tweets we want to accualy share how many tweets we want to extract
    def get_user_timeline_tweets(self,num_tweets):
        tweets=[]
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets


    def get_friend_list(self, num_friends):
        friend_list=[]
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    
    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets=[]
        for tweet in Cursor(self.twitter_client.home_timeline_tweets, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets






# # # # # TWITTER AUTHENTICATE # # # # #
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth=OAuthHandler(keys.CONSUMER_KEY,keys.CONSUMER_SECRET)
        auth.set_access_token(keys.ACCESS_TOKEN,keys.ACCESS_TOKEN_SECRET)
        return auth




# # # # # TWITTER STREAMER # # # # #

#CLASS FOR STREAMING AND PROCESSING LIVE TWEETS
class TwitterStreamer():
    def __init__(self):
        self.twitter_authenticator=TwitterAuthenticator()



    def stream_tweets(self,fetched_tweets_filename,hash_tag_list):
        #this handles the connection to the twitter streaming API
        listener=TwitterListener()
        auth=self.twitter_authenticator.authenticate_twitter_app()
        #this funstion provides me to stream all the tweets about hash_tag_list. You can hard code here like hash_tag_list="covid19" 
        stream=Stream(auth,listener)
        stream.filter(track= [hash_tag_list])


#THIS IS A BASIC LISTENER CLASS THAT JUST PRINTS RECEIVED TWEETS TO STDOUT

class TwitterListener(StreamListener):

    def __init__(self, fetched_tweets_filename=None):
        if fetched_tweets_filename is None:
         fetched_tweets_filename = {}
        else:
            self.fetched_tweets_filename = data
        self.fetched_tweets_filename=fetched_tweets_filename

    def on_data(self,data):
        try: 
            print(data)
            with open(self.fetched_tweets_filename,'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True


    def on_error(self,status):
        if status==420:
            #returnin false on_data methon in case rate limit occurs.
            return False
        print(status)

#functionality for analyzing and catogarizing content from tweets
class TweetsAnalyzer():
    def tweets_to_data_frame(self,tweets):
        df=pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])    
        df['id']=np.array([tweet.id for tweet in tweets])
        df['len']=np.array([len(tweet.text) for tweet in tweets])
        df['date']=np.array([tweet.created_at for tweet in tweets])
        df['source']=np.array([tweet.source for tweet in tweets])
        df['likes']=np.array([tweet.favorite_count for tweet in tweets])
        df['retweets']=np.array([tweet.retweet_count for tweet in tweets])
        return df

if __name__=="__main__":

    twitter_client=TwitterClient()
    tweet_analyzer=TweetsAnalyzer()
    api=twitter_client.get_twitter_client_api()
    tweets= api.user_timeline(screen_name='realDonaldTrump',count=20)
    df=tweet_analyzer.tweets_to_data_frame(tweets)

   






    
    # ###tweet analysing this code below helps us to read 10 tweet content. Like head of the tweet
    # twitter_client=TwitterClient()
    # tweet_analyzer=TweetsAnalyzer()

    # api=twitter_client.get_twitter_client_api()
    # #user_timeline is a function from client
    # tweets= api.user_timeline(screen_name='realDonaldTrump',count=20)
    # df=tweet_analyzer.tweets_to_data_frame(tweets)
    # print(df.head(10))
    # ###
  
  
  
  
  
  
    # hash_tag_list=["covid19","covid"]
    # for hash_tag in hash_tag_list:
    #     hash_tag_list=", ".join(hash_tag)

    # fetched_tweets_filename="tweets.txt"

    # #when we write like thi it stream "pycon" user and its 1 tweet
    # twitter_client=TwitterClient("PyCon")
    # print(twitter_client.get_user_timeline_tweets(1))

    # #when we write like thi it streams us fetched_tweets_filename and hash_tag_list
    # # twitter_streamer= TwitterStreamer()
    # # twitter_streamer.stream_tweets(fetched_tweets_filename,hash_tag_list)