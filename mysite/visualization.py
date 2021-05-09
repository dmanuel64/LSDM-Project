import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from pathlib import Path
from datetime import date, time
from textblob import TextBlob
from wordcloud import WordCloud
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS

class Bar:

    def __init__(self):
        self.all_vax = ['covaxin', 'sinopharm', 'sinovac', 'moderna', 'pfizer', 'biontech', 'oxford', 'astrazeneca', 'sputnik']

    def monthly_tweets(self):
        """[Get monthly number of tweets]

        Returns:
            [string]: [month labels]
            [integers]: [values]
        """        

        df = pd.read_csv("data/vaccination_tweets.csv")
        df['date']=pd.to_datetime(df.date)
        df = df.sort_values(by='date')
        df['date'] = df['date'].dt.strftime('%m/%y')

        line = df.groupby(['date'], sort=False).count().reset_index()
        line['count'] = line['text']
        line = line[['date', 'count']]

        return list(line['date'].values), list(line['count'].values)

    def tweets_bar(self):
        """[Get daily number of tweets]

        Returns:
            [string]: [day labels]
            [integers]: [values]
        """        

        df = pd.read_csv("data/vaccination_tweets.csv")
        df['date'] =pd.to_datetime(df.date)
        df = df.sort_values(by='date')

        df['date'] = df['date'].dt.strftime('%d/%m')       

        # let's inspect how many tweets there were with respect to time
        timeline = df.groupby(['date'], sort=False).count().reset_index()
        timeline['count'] = timeline['text']
        timeline = timeline[['date', 'count']]

        return list(timeline['date'].values), list(timeline['count'].values)

    def user_engagement_bar(self, engagement_type):
        """[Get users with most retweets, favorites, and engagements]

        Args:
            engagement_type ([string]): ["retweets", "favorites", "total_engagement]

        Returns:
            [string]: [user name labels]
            [integers]: [values]
        """        

        df=pd.read_csv('data/vaccination_tweets.csv')
        df['total_engagement']=df['retweets']+df['favorites']

        title = "Account " + engagement_type

        if engagement_type == "retweets":
            data = df.groupby('user_name',as_index=False).agg({'retweets':'sum'}).sort_values('retweets',ascending=False).head(10)
            y = "retweets"
        elif engagement_type == "favorites":
            data = df.groupby('user_name',as_index=False).agg({'favorites':'sum'}).sort_values('favorites',ascending=False).head(10)
            y = "favorites"
        elif engagement_type == "total_engagement":
            data = df.groupby('user_name',as_index=False).agg({'total_engagement':'sum'}).sort_values('total_engagement',ascending=False).head(10)
            y = "total_engagement"            

        return list(data['user_name'].values), list(data[y].values)

    def verified_bar(self):
        """[Get count of verified and non verified accounts]

        Returns:
            [string]: [verified or non verified labels]
            [integers]: [values]
        """        

        df = pd.read_csv("data/vaccination_tweets.csv")
        df.drop(columns=['id'], inplace=True)
        df = df.drop_duplicates('text')
        df['date'] = pd.to_datetime(df['date']).dt.date


        verified = df.loc[df.user_verified == True].shape[0]
        non_verified = df.loc[df.user_verified == False].shape[0]
        
        data = [verified, non_verified]
        labels = ['verified', 'non_verified']
        
        return (labels, data)

    def source_max(self, k):
        """[Get top sources]

        Args:
            k ([integer]): [top k sources]

        Returns:
            [string]: [sources labels]
            [integers]: [values]
        """        
        df = pd.read_csv("data/vaccination_tweets.csv")
        src = df['source'].value_counts().sort_values(ascending=False)
        source = src.head(k)

        return list(source.index), list(source.values)

    def per_day(self):
        """[Get number of tweets per weekdays]

        Returns:
            [string]: [weekday labels]
            [integers]: [values]
        """        

        df = pd.read_csv("data/vaccination_tweets.csv")
        df["date"] = pd.to_datetime(df["date"])
        df["Month"] = df["date"].apply(lambda x : x.month)
        df["day"] = df["date"].apply(lambda x : x.dayofweek)
        dmap = {0:'Sun', 1:'Mon',2:'Tue',3:'Wed',4:'Thu',5:'Fri',6:'Sat'}
        df["day"] = df["day"].map(dmap)

        df = df.groupby(['day']).count().reset_index()
        df['count'] = df['text']
        df = df[['day', 'count']]

        cats = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        df.day = pd.Categorical(df.day,categories=cats)
        df = df.sort_values('day')
        
        return list(df['day'].values), list(df['count'].values)

    def top_hashtag(self, k):
        """[Get top hashtags]

        Args:
            k ([integer]): [top k hashtags]

        Returns:
            [string]: [hashtags labels]
            [integers]: [values]
        """        

        df = pd.read_csv("data/vaccination_tweets.csv")
        htags = pd.DataFrame(df['hashtags'].value_counts()).reset_index()
        htags = htags[htags['index'] != 'No HashTag']
        htags = htags.rename(columns={'index': 'Hashtags', 'hashtags': 'counts'})[:k]

        return list(htags['Hashtags'].values), list(htags['counts'].values)

    def hashtag_retweet_favorite(self, engagement_type, k):
        """[Get hashtags with most retweets or favorites]

        Args:
            engagement_type ([string]): ["retweets" or "favorites]
            k ([integer]): [top k hashtags with most specific engagement type]

        Returns:
            [string]: [hashtags labels]
            [integers]: [retweets or favorites values]
        """        

        df = pd.read_csv("data/vaccination_tweets.csv")
        df = df[pd.notnull(df['hashtags'])]

        if engagement_type == "retweets":
            df_sort = df.sort_values('retweets', ascending=False)
        elif engagement_type == "favorites":
            df_sort = df.sort_values('favorites', ascending=False)

        return list(df_sort[:k]['hashtags'].values), list(df_sort[:k][engagement_type].values)  

    def top_location(self, k):
        """[Get top locations]

        Args:
            k ([integer]): [top k locations]

        Returns:
            [string]: [location labels]
            [integers]: [values]
        """        

        df = pd.read_csv("data/vaccination_tweets.csv")
        data = df["user_location"].value_counts().values[0:5], df["user_location"].value_counts().index[:k]

        return list(data[1]), list(data[0])

    def daily_engagement(self, engagement_type):
        """[Get daily engagement such as retweets, favorites, or engagement]

        Args:
            engagement_type ([string]): ["retweet", "favorites", "total engagement]

        Returns:
            [string]: [date labels]
            [integers]: [values]
        """

        df = pd.read_csv("data/vaccination_tweets.csv")
        df['date']=pd.to_datetime(df['date'])

        if engagement_type == "total_engagement":
            df['total_engagement']=df['retweets']+df['favorites']
            df = df.sort_values(by='date')
            df['date'] = df['date'].dt.strftime('%d/%m/%y')       
            day_month = df.groupby('date', sort=False, as_index=False).agg({'total_engagement':'sum'})
        elif engagement_type == "retweets":
            df = df.sort_values(by='date')
            df['date'] = df['date'].dt.strftime('%d/%m/%y')       
            day_month = df.groupby('date', sort=False, as_index=False).agg({'retweets':'sum'})
        elif engagement_type == "favorites":
            df = df.sort_values(by='date')
            df['date'] = df['date'].dt.strftime('%d/%m/%y')       
            day_month = df.groupby('date', sort=False, as_index=False).agg({'favorites':'sum'})            

        return list(day_month['date'].values), list(day_month[engagement_type].values)   

class Pie:
    def verified_pie(self):
        """[Get number of verified vs unverified]

        Returns:
            [string]: [verified or non verified labels]
            [integers]: [values]
        """        
        df = pd.read_csv("data/vaccination_tweets.csv")
        verified = df[df["user_verified"]==True].shape[0]
        non_verified = df[df["user_verified"]==False].shape[0]
        
        labels = ['not_verified', 'verified']
        sizes = [non_verified, verified]

        return labels, sizes

    def top_pie(self, k, col_name):
        """[Get top information ]

        Args:
            k ([integer]): [top k information]
            col_name ([string]): [information of interest]

        Returns:
            [string]: [top information labels]
            [integers]: [values]
        """        
        df = pd.read_csv("data/vaccination_tweets.csv")
        top_tags=df[col_name].value_counts().sort_values(ascending=False)

        return list(top_tags[:k].index) , list(top_tags[:k].values)

    def sentiment_pie(self):
        """[Get sentimental analysis ]

        Returns:
            [string]: [sentiment "positive" "neutral" "negative"]
            [integers]: [values]
        """        
        df = pd.read_csv("data/vaccination_tweets.csv")
        neutral_thresh = 0.05

        # Obtain polarity scores generated by TextBlob
        df['score'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)

        # Convert polarity score into sentiment categories
        df['sentiment'] = df['score'].apply(lambda c: 'Positive' if c >= neutral_thresh else ('Negative' if c <= -(neutral_thresh) else 'Neutral'))

        positive = df[df['sentiment'].str.contains("Positive")].shape[0]
        neutral  = df[df['sentiment'].str.contains("Neutral")].shape[0]
        negative = df[df['sentiment'].str.contains("Negative")].shape[0]

        labels = ['positive', 'neutral', 'negative']
        sizes = [positive, neutral, negative]

        return labels, sizes

class Wordcloud:
    def text_wordcloud(self, col_name):
        df = pd.read_csv("data/vaccination_tweets.csv", quotechar='"', delimiter=',').dropna()

        data = df[col_name]
        text = " ".join(t for t in data.dropna())
        stop_words = set(STOPWORDS)
        stop_words.update(["t", "co", "https", "amp", "U"])

        wordcloud = WordCloud(stopwords=stop_words, scale=4, max_font_size=50, max_words=500,background_color="black").generate(text)
        fig = plt.figure(figsize=(16,4))
        plt.axis('off')
        
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.savefig("static/img/"+col_name+".png", bbox_inches='tight')

    def country_map(self):
        df = pd.read_csv("data/vaccination_tweets.csv")
        loc_df = df['user_location'].str.split(',',expand=True)
        loc_df=loc_df.rename(columns={0:'fst_loc',1:'snd_loc'})
        # Remove Spaces 
        loc_df['snd_loc'] = loc_df['snd_loc'].str.strip()

        # Rename States 
        state_fix = {'Ontario': 'Canada','United Arab Emirates': 'UAE','TX': 'USA','NY': 'USA'
                        ,'FL': 'USA','England': 'UK','Watford': 'UK','GA': 'USA','IL': 'USA'
                        ,'Alberta': 'Canada','WA': 'USA','NC': 'USA','British Columbia': 'Canada','MA': 'USA','ON':'Canada'
                    ,'OH':'USA','MO':'USA','AZ':'USA','NJ':'USA','CA':'USA','DC':'USA','AB':'USA','PA':'USA','SC':'USA'
                    ,'VA':'USA','TN':'USA','New York':'USA','Dubai':'UAE','CO':'USA'}

        loc_df = loc_df.replace({"snd_loc": state_fix}) 
        df_loc = pd.DataFrame(loc_df['snd_loc'].value_counts()[:20]).reset_index()

        fig = px.choropleth(df_loc, locations = df_loc['index'], color = df_loc['snd_loc'], locationmode='country names', 
                                color_continuous_scale = px.colors.sequential.Inferno)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        # fig.layout.autosize = True
        fig.layout.height = 300
        fig.layout.width = 1000
        fig.write_image("static/img/map.png")  

class Line:

    def month_engagement(self):
        """[Get monthly engagement]

        Returns:
            [strings]: [months]
            [integers]: [values]            
        """        
        df = pd.read_csv("data/vaccination_tweets.csv")
        df['date']=pd.to_datetime(df['date'])
        df['total_engagement']=df['retweets']+df['favorites']

        df = df.sort_values(by='date')
        df['date'] = df['date'].dt.strftime('%m/%y')       
        day_month = df.groupby('date', sort=False, as_index=False).agg({'total_engagement':'sum'})

        return list(day_month['date'].values), list(day_month['total_engagement'].values)

class Sentiment:
    def __init__(self) -> None:
        self.df = pd.read_csv("data/vaccination_tweets.csv")
        analyser = SentimentIntensityAnalyzer()
        scores=[]
        sentiment=[]

        for i in range(len(self.df['text'])):
            score = analyser.polarity_scores(self.df['text'][i])
            score=score['compound']
            scores.append(score)

        for i in scores:
            if i>=0.05: sentiment.append('Positive')
            elif i<=(-0.05): sentiment.append('Negative')
            else: sentiment.append('Neutral')

        self.df['sentiment']=pd.Series(np.array(sentiment))

    def sentiment_date(self, sentiment_type):
        """[Get daily sentimental analysis positive, neutral, negative]

        Args:
            sentiment_type ([integer]): [sentiment "positive" "neutral" "negative"]

        Returns:
            [strings]: [dates]
            [integers]: [values]     
        """        
        self.df["date"] = pd.to_datetime(self.df.date) 

        timeline = self.df.resample('D', on='date')["sentiment"].value_counts().unstack(1)
        timeline.reset_index(inplace=True)
        timeline = timeline.melt("date", var_name='sentiment',  value_name='vals')
        timeline['date'] = timeline['date'].dt.strftime('%d/%m')   

        if sentiment_type == "positive":
            data = timeline[timeline['sentiment'].str.contains("Positive")]
        elif sentiment_type == "negative":
            data = timeline[timeline['sentiment'].str.contains("Negative")]
        elif sentiment_type == "neutral":
            data = timeline[timeline['sentiment'].str.contains("Neutral")]   

        return list(data['date'].values), list(data['vals'].values)

    def sentiment_bar(self):
        """[Get total sentimental analysis]

        Returns:
            [string]: [sentiment labels]
            [integers]: [values]
        """

        temp = self.df.groupby('sentiment').count()['text'].reset_index().sort_values(by='text',ascending=False)

        return list(temp['sentiment'].values), list(temp['text'].values)

    def accounts_sentiment(self, sentiment_type, k):
        """[Get top accounts with most positive, neutral, or negative]

        Args:
            sentiment_type ([string]): ["positive", "neutral", "negative"]
            k ([integer]): [description]

        Returns:
            [string]: [user_name labels]
            [integers]: [values]
        """        

        if sentiment_type=="positive":      
            data=self.df[(self.df.sentiment== "Positive")].drop_duplicates(subset=["user_name"])\
                .sort_values(by=["user_followers"], ascending=False)[["user_name", "user_followers"]][:k]
        elif sentiment_type=="neutral":          
            data=self.df[(self.df.sentiment== "Neutral")].drop_duplicates(subset=["user_name"])\
                .sort_values(by=["user_followers"], ascending=False)[["user_name", "user_followers"]][:k]
        elif sentiment_type=="negative":          
            data=self.df[(self.df.sentiment== "Negative")].drop_duplicates(subset=["user_name"])\
                .sort_values(by=["user_followers"], ascending=False)[["user_name", "user_followers"]][:k]                                

        return list(data['user_name'].values), list(data['user_followers'].values)     