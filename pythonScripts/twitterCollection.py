# imports used
import pandas as pd
import tweepy
import matplotlib.pyplot as plot
import numpy as np

# Twitter credentials to access Twitter API
consumer_key = "wauZsdG55Ly7VPFQ6bMOpaTxS"
consumer_secret = "DG8l6hGKyYpZk0MMlGxpeIKl1iyRfZrZLE1BxNntKmObGbfGwW"
token_key = "1353538103529664514-kKPU3vb8Yi7xkGwmFVWz4qt8iNCYcl"
token_secret = "hOorZorcO1qYjSSEKsk0GSSj7mWntObzHyWPFAjTffzQt"
authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(token_key, token_secret)
api = tweepy.API(authentication)


def twitter(string):
    # initialize required variables to gather tweets
    hashtag = string  # string variable for hashtag to look update
    date = "2021-04-15"  # string variable to search for tweets since date
    num_tweet = 1000  # integer variable for number of tweets to be collected

    # create dataframe to use for analysis
    df = pd.DataFrame(columns=['username', 'location', 'created', 'followers', 'timesRetweeted', 'text', 'hashtags'])
    # used to search through twitter
    tweets = tweepy.Cursor(api.search, q=hashtag, lang="en", since=date, tweet_mode='extended').items(num_tweet)

    # initializations to iterate tweets
    tweetList = [tweet for tweet in tweets]  # get information of each tweet
    i = 1  # counter for iteration
    highestFollower = 0
    highestRetweet = 0

    for tweet in tweetList:
        username = tweet.user.screen_name
        location = tweet.user.location
        created = tweet.created_at
        followers = tweet.user.followers_count
        retweet_count = tweet.retweet_count
        hashtags = tweet.entities['hashtags']

        # in case tweet is a retweet
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:  # not a retweet
            text = tweet.full_text
        if followers > highestFollower:
            follower = username
            highestFollower = followers
        if retweet_count > highestRetweet:
            retweet = username
            highestRetweet = retweet_count
        # store all data that we want into separate variable
        ith_tweet = [username, location, created, followers, retweet_count, text, hashtags]
        # append tweet to dataframe
        df.loc[len(df)] = ith_tweet

    # send dataframe into a csv file for data analytics
    geo = df['location'].value_counts()
    geo = geo.head(10)
    barGraph(geo)

    return retweet, follower

def barGraph(geo):
    plot.figure(figsize=(720 / 96, 320 / 96), dpi=96)
    #plot.rcParams['font.sans-serif'] = ['SimHei']
    #plot.rcParams['axes.unicode_minus']=False
    plot.bar(range(len(geo)), geo)
    plot.xlabel("Location")
    plot.ylabel("# of Tweets")
    plot.xticks(np.arange(10), geo.index, rotation=45)
    plot.tight_layout()
    plot.savefig('static/img/testBar.png', dpi=96)
    plot.clf()
    plot.close()
