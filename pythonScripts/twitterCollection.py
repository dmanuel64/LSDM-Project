# imports used
import pandas as pd
import tweepy

# Twitter credentials to access Twitter API
consumer_key = "z28wXtL4NjuD3n3G88n1o0BFw"
consumer_secret = "DSebmaKfKmjqRLbncFcIayR8Q96de6nCXFI0O1qdL8YST5JU9L"
token_key = "3270448494-agr0ukiuC17nn3vXVpIGoctvaQu7kKFn7E2REfk"
token_secret = "VsJdh60xllZAlq7IJmjR4I2HlEuGLeRAoSZd3xYefe8dT"
authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(token_key, token_secret)
api = tweepy.API(authentication)


def twitter(string):
    # initialize required variables to gather tweets
    hashtag = string  # string variable for hashtag to look update
    date = "2021-04-15"  # string variable to search for tweets since date
    num_tweet = 100  # integer variable for number of tweets to be collected

    # create dataframe to use for analysis
    df = pd.DataFrame(columns=['username', 'location', 'created', 'followers', 'timesRetweeted', 'text', 'hashtags'])
    # used to search through twitter
    tweets = tweepy.Cursor(api.search, q=hashtag, lang="en", since=date, tweet_mode='extended').items(num_tweet)

    # initializations to iterate tweets
    tweetList = [tweet for tweet in tweets]  # get information of each tweet
    i = 1  # counter for iteration

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
        # store all data that we want into separate variable
        ith_tweet = [username, location, created, followers, retweet_count, text, hashtags]
        # append tweet to dataframe
        df.loc[len(df)] = ith_tweet

    # send dataframe into a csv file for data analytics
    filename = "twitterData.csv"
    df.to_csv("data/" + filename)
