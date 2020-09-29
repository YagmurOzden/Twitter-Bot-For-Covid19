from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import date


#this is where i put my CONSUMER_KEY etc.
import keys

# # # # # TWITTER AUTHENTICATE # # # # #
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth=OAuthHandler(keys.CONSUMER_KEY,keys.CONSUMER_SECRET)
        auth.set_access_token(keys.ACCESS_TOKEN,keys.ACCESS_TOKEN_SECRET)
        return auth



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

class Screenshot():
    def __init__(self):
        self.browserProfile=webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs',{'intl.accept_languages': 'en,en_US'})
        self.browser=webdriver.Chrome('chromedriver.exe',chrome_options=self.browserProfile)   
    def Screenshot(self):

        url="https://covid19.saglik.gov.tr/"
        self.browser.get(url)
        self.browser.maximize_window()
        data= self.browser.find_element_by_xpath("/html/body/section[2]/div/div/div")
        time.sleep(5)
        ss= data.screenshot_as_png
        time.sleep(5)

        with open(str(date.today()) +'.png', 'wb') as f:
            f.write(ss)       
        self.browser.close()

if __name__=="__main__":

    ss=Screenshot()
    ss.Screenshot()
    twitter_client=TwitterClient()
    api=twitter_client.get_twitter_client_api()


    # Upload images and get media_ids
    filenames = [str(date.today()) + '.png']
    media_ids = []
    for filename in filenames:
        res = api.media_upload(filename)
        media_ids.append(res.media_id)
    # Tweet with multiple images
    api.update_status(status='Vaka sayısı:', media_ids=media_ids)