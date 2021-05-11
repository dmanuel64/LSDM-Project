import os
import re
import pandas as pd
from textblob import TextBlob


class Table:

    def __init__(self) -> None:
        self.df = pd.read_csv("data/vaccination_tweets.csv")
        self.df['polarity'] = self.df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)
        self.df['subjectivity'] = self.df['text'].apply(lambda x: TextBlob(x).sentiment.subjectivity)

    def search(self, query):
        """[Search for keywords in a given field]

        Args:
            query ([string]): [keyword to search]

        Returns:
            [dataframe]: [table with results from search]
        """           
        df = pd.read_csv("data/vaccination_tweets.csv")
        df.drop(columns=['id'], inplace=True)
        df.dropna()

        df = df[['user_name', 'user_location', 'user_followers', 'user_verified',
                        'text', 'hashtags', 'source', 'retweets', 'favorites', 'is_retweet']]

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

        return results

    def input_sentiment(self, sentence):
        polarity = TextBlob(sentence).sentiment.polarity
        subjectivity = TextBlob(sentence).sentiment.subjectivity

        return ( polarity, subjectivity)

    """Already done by table functions"""
    # def top_retweet_favorites(self, k, engagement_type):
    #     df = pd.read_csv("data/vaccination_tweets.csv")

    #     df = df.sort_values(by=engagement_type, ascending=False)[['user_name', 'user_location', 'user_followers', 'user_verified',
    #                             'text', 'hashtags', 'source', 'retweets', 'favorites', 'is_retweet']]
    #     return df.head(n=k)

    def top_polarity(self, sentiment_type, k):
        """[Get the most negative or positive tweets]

        Args:
            sentiment_type ([string]): [negative or positive]
            k ([integer]): [get the top k tweets of specified sentiment]

        Returns:
            [dataframe]: [table with type k tweets of specified sentiment]
        """        
        if sentiment_type == "negative":
            # inspect the most negatively charged tweets
            data = self.df.sort_values(by='polarity', ascending=True)[['text', 'polarity', 'subjectivity']].reset_index(drop=True)
        elif sentiment_type == "positive":
            # inspect the most positively charged tweets
            data = self.df.sort_values(by='polarity', ascending=False)[['text', 'polarity', 'subjectivity']].reset_index(drop=True)

        return data.head(n=k)

    def top_subjectivity(self, subjectivity_type, k):    
        """[Get the most subjective or objective tweets]

        Args:
            sentiment_type ([string]): [subjective or objective]
            k ([integer]): [get the top k tweets of specified subectivity]

        Returns:
            [dataframe]: [table with type k tweets of specified subectivity]
        """        
        if subjectivity_type == "objective":
            # inspect the most objective tweets            
            data = self.df.sort_values(by='subjectivity', ascending=True)[['text', 'polarity', 'subjectivity']].reset_index(drop=True)
        if subjectivity_type == "subjective":
            # inspect the most subjective tweets (NOTE: subjectivity scale ranges from 0 to 1)
            data = self.df.sort_values(by='subjectivity', ascending=False)[['text', 'polarity', 'subjectivity']].reset_index(drop=True)

        return data.head(n=k)