import os
import re
import pandas as pd
from textblob import TextBlob


class Table:

    def search(self, query):        
        df = pd.read_csv("data/vaccination_tweets.csv")
        df.drop(columns=['id'], inplace=True)
        df.dropna()

        if ':' in query: 
            print("ere")
            type, keywords = query.split(":")
            if type not in list(df):
                type = "text"
        else: 
            type = "text"
            keywords = query

        keywords = keywords.strip()
        results = df[df[type].str.contains("(?i)"+keywords) == True]
        results = results[['user_name', 'user_location', 'user_followers', 'user_verified',
                                'text', 'hashtags', 'source', 'retweets', 'favorites', 'is_retweet']]

        return results

    def input_sentimental(self, sentence):
        polarity = TextBlob(sentence).sentiment.polarity
        subjectivity = TextBlob(sentence).sentiment.subjectivity

        return ( polarity, subjectivity)

    def top_retweet_favorites(self, k, engagement_type):
        df = pd.read_csv("data/vaccination_tweets.csv")

        if engagement_type == "retweets":
            df = df.sort_values(by='retweets', ascending=False)[['text', 'date', 'user_name', 'user_location', 'hashtags', 'favorites', 'retweets']].head(n=k)
        elif engagement_type == "favorites":            
            df = df.sort_values(by='favorites', ascending=False)[['text', 'date', 'user_name', 'user_location', 'hashtags', 'favorites', 'retweets']].head(n=k)

        return df

    def top_polarity(self, sentiment_type, k):
        df = pd.read_csv("data/vaccination_tweets.csv")
        df['polarity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)
        df['subjectivity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.subjectivity)

        if sentiment_type == "negative":
            # inspect the most negatively charged tweets
            df = df.sort_values(by='polarity', ascending=True)[['text', 'polarity', 'subjectivity']].reset_index(drop=True).head(n=k)
        elif sentiment_type == "positive":
            # inspect the most positively charged tweets
            df = df.sort_values(by='polarity', ascending=False)[['text', 'polarity', 'subjectivity']].reset_index(drop=True).head(n=k)

        return df

    def top_subjectivity(self, subjectivity_type, k):    
        df = pd.read_csv("data/vaccination_tweets.csv")
        df['polarity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)
        df['subjectivity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.subjectivity)

        if subjectivity_type == "objective":
            # inspect the most objective tweets            
            df = df.sort_values(by='subjectivity', ascending=True)[['text', 'polarity', 'subjectivity']].reset_index(drop=True).head(n=k)
        if subjectivity_type == "subjective":
            # inspect the most subjective tweets (NOTE: subjectivity scale ranges from 0 to 1)
            df = df.sort_values(by='subjectivity', ascending=False)[['text', 'polarity', 'subjectivity']].reset_index(drop=True).head(n=k)

        return df