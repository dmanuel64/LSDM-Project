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
        self.bar_dir = os.path.join("figures", "bar")
        Path(self.bar_dir).mkdir(parents=True, exist_ok=True)
        self.all_vax = ['covaxin', 'sinopharm', 'sinovac', 'moderna', 'pfizer', 'biontech', 'oxford', 'astrazeneca', 'sputnik']

    def plot_bar(self, data, x, y, title):
        fig = px.bar(data, x=x, y=y, labels={x: 'Date', y: 'Tweet Count'}, title=title)
        fig.write_image(os.path.join(self.bar_dir, title + ".png"))

    def plot_sns(self, data, x, title):
        plt.figure(figsize=(8, 8))
        # sns.countplot(x=x, data=data)
        # plt.savefig(os.path.join(self.bar_dir, title + ".png"))        
        return

    def monthly_tweets(self):
        df=pd.read_csv('data/vaccination_tweets.csv')
        df['date']=pd.to_datetime(df.date)
        df = df.sort_values(by='date')
        df['date'] = df['date'].dt.strftime('%m/%y')

        # df['total_engagement']=df['retweets']+df['favorites']
        # line = df.groupby('date', sort=False, as_index=False).agg({'total_engagement':'sum'})
        
        line = df.groupby(['date'], sort=False).count().reset_index()
        line['count'] = line['text']
        line = line[['date', 'count']]

        # self.plot_bar(line, x, y, title)

        return ( list(line['date'].values), list(line['count'].values))

    def tweets_bar(self):
        df=pd.read_csv('data/vaccination_tweets.csv')
        df['date'] =pd.to_datetime(df.date)
        df = df.sort_values(by='date')

        df['date'] = df['date'].dt.strftime('%d/%m')       

        # let's inspect how many tweets there were with respect to time
        timeline = df.groupby(['date'], sort=False).count().reset_index()
        timeline['count'] = timeline['text']
        timeline = timeline[['date', 'count']]

        x = "date"
        y = "count"
        title = "count"
        # self.plot_bar(timeline, x, y, title)

        return (list(timeline['date'].values), list(timeline['count'].values), title)

    def sentiment_bar(self, df):
        df=pd.read_csv('vaccination_tweets.csv')
        df = df.drop_duplicates('text')
        df['date'] = pd.to_datetime(df['date']).dt.date
        df['polarity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)
        df['subjectivity'] = df['text'].apply(lambda x: TextBlob(x).sentiment.subjectivity)
        # polarity values ranging from -1 to 1 are really useful for sentiment analysis
        # but let's convert our data to 3 classes (negative, neutral, and positive) so that we can visualize it
        criteria = [df['polarity'].between(-1, -0.01), df['polarity'].between(-0.01, 0.01), df['polarity'].between(0.01, 1)]
        values = ['negative', 'neutral', 'positive']
        df['sentiment'] = np.select(criteria, values, 0)

        timeline = df.groupby(['date']).agg(np.nanpmean).reset_index()
        timeline['count'] = df.groupby(['date']).count().reset_index()['retweets']
        timeline = timeline[['date', 'count', 'polarity', 'retweets', 'favorites', 'subjectivity']]
        timeline["polarity"] = timeline["polarity"].astype(float)
        timeline["subjectivity"] = timeline["subjectivity"].astype(float)
        timeline.sort_values(by='polarity', hmascending=False)

        x='date'
        y='count'
        
        # self.plot_bar(timeline, x, y, title='polarity')
        # self.plot_bar(timeline, x, y, title='subjectivity')

    def user_engagement_bar(self, engagement_type):
        df=pd.read_csv('data/vaccination_tweets.csv')
        df['total_engagement']=df['retweets']+df['favorites']

        x = "user_name"
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

        # self.plot_bar(data, x, y, title)

        return (list(data['user_name'].values), list(data[y].values))

    def verified_bar(self):
        df = pd.read_csv("data/vaccination_tweets.csv")
        df.drop(columns=['id'], inplace=True)
        df = df.drop_duplicates('text')
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        x = 'user_verified'
        title = "Verified user accounts or not "

        verified = df.loc[df.user_verified == True].shape[0]
        non_verified = df.loc[df.user_verified == False].shape[0]
        
        data = [verified, non_verified]
        labels = ['verified', 'non_verified']
        
        # self.plot_sns(df, x,title)
        return (labels, data, title)

    def source_max(self, k):
        df = pd.read_csv("data/vaccination_tweets.csv")
        # plt.figure(figsize=(8, 8))
        src = df['source'].value_counts().sort_values(ascending=False)
        source = src.head(5)
        # source.plot.bar()
        # plt.title('Source with maximum number of tweets')
        # plt.xlabel('User Source')
        # plt.ylabel('Tweet Count')
        # #15
        # plt.savefig(os.path.join(self.bar_dir, "max_tweet.png"))

        return (list(source.index), list(source.values))

    def per_day(self):
        df=pd.read_csv('data/vaccination_tweets.csv')
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

        x = "day"
        title = "Day with maximun tweets"

        # self.plot_sns(df, x,title)
        
        return (list(df['day'].values), list(df['count'].values), title)

    def top_hashtag(self, k):
        df=pd.read_csv('data/vaccination_tweets.csv')
        htags = pd.DataFrame(df['hashtags'].value_counts()).reset_index()
        htags = htags[htags['index'] != 'No HashTag']
        htags = htags.rename(columns={'index': 'Hashtags', 'hashtags': 'counts'})[:k]
        
        # plt.figure(figsize=(8, 8))
        # sns.barplot(x='Hashtags', y='counts', data=htags)

        # h.set_title('Top 10 Hashtag Most Used')
        # h.set_xlabel('#Hashtags')
        # h.set_ylabel('Number of Tags')

        # plt.xticks(rotation=90)
        # plt.savefig(os.path.join(self.bar_dir, "177top_hashtag.png"))

        return(list(htags['Hashtags'].values), list(htags['counts'].values))

    def hashtag_retweet(self, k):
        df=pd.read_csv('data/vaccination_tweets.csv')
        df = df[pd.notnull(df['hashtags'])]
        df_sort = df.sort_values('retweets', ascending=False)
        # retweet = df[df['hashtags'].isin(top_10)]
        
        # plt.figure(figsize=(8, 8))
        # k=sns.barplot(x='hashtags', y='retweets', data=retweet)

        # k.set_title('Top 10 Hashtag Most Retweeted')
        # k.set_xlabel('#Hashtags')
        # k.set_ylabel('Number of Reweets')

        # plt.xticks(rotation=90)
        #18
        # plt.savefig(os.path.join(self.bar_dir, "18top_hashtag_retweet.png"))

        return (list(df_sort[:k]['hashtags'].values), list(df_sort[:k]['retweets'].values))

    def hashtag_favorite(self, k):
        df=pd.read_csv('data/vaccination_tweets.csv')
        df = df[pd.notnull(df['hashtags'])]
        df_sort = df.sort_values('favorites', ascending=False)
        # retweet = df[df['hashtags'].isin(top_10)]
        
        # plt.figure(figsize=(8, 8))
        # k=sns.barplot(x='hashtags', y='retweets', data=retweet)

        # k.set_title('Top 10 Hashtag Most Retweeted')
        # k.set_xlabel('#Hashtags')
        # k.set_ylabel('Number of Reweets')

        # plt.xticks(rotation=90)
        #18
        # plt.savefig(os.path.join(self.bar_dir, "18top_hashtag_retweet.png"))

        return (list(df_sort[:k]['hashtags'].values), list(df_sort[:k]['favorites'].values))        

    def top_location(self, k):
        df=pd.read_csv('data/vaccination_tweets.csv')
        # plt.figure(figsize=(8, 8))
        data = df["user_location"].value_counts().values[0:5], df["user_location"].value_counts().index[:k]
        # sns.barplot(df["user_location"].value_counts().values[0:5], df["user_location"].value_counts().index[0:5])
        # plt.title("Top 5 Places with maximum tweets")
        # plt.xlabel("Number of tweets")
        # plt.ylabel("Country")
        #19
        # plt.savefig(os.path.join(self.bar_dir, "19top_places.png"))
        # return (list(data.index), list(data.values))
        return (list(data[1]), list(data[0]))

    def daily_engagement(self, engagement_type):
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


        # self.plot_line(x, y, day_month, title)
        return (list(day_month['date'].values), list(day_month[engagement_type].values))   
    # print(f" Data Available since {df.date.min()}")
    # print(f" Data Available upto {df.date.max()}")

    def sentiment_bar_once_again(self, filename):
        df=pd.read_csv('vaccination_tweets.csv')

        analyser = SentimentIntensityAnalyzer()

        scores=[]

        for i in range(len(df['text'])):
            score = analyser.polarity_scores(df['text'][i])
            score=score['compound']
            scores.append(score)

        sentiment=[]

        for i in scores:
            if i>=0.05: sentiment.append('Positive')
            elif i<=(-0.05): sentiment.append('Negative')
            else:sentiment.append('Neutral')
                
        df['sentiment']=pd.Series(np.array(sentiment))

        temp = df.groupby('sentiment').count()['text'].reset_index().sort_values(by='text',ascending=False)

        # plt.figure(figsize=(8, 8))
        # sns.countplot(x='sentiment',data=df)
        #27
        # plt.savefig(os.path.join(self.bar_dir, "27sentiment.png"))

        # plt.figure(figsize=(8, 8))
        # sns.barplot(x="user_verified", y="favorites", hue="sentiment", data=df)
        # #29
        # plt.savefig(os.path.join(self.bar_dir, "29verified_favorites.png"))

        # plt.figure(figsize=(8, 8))
        # sns.barplot(x="user_verified", y="retweets", hue="sentiment", data=df)
        # #30
        # plt.savefig(os.path.join(self.bar_dir, "30verified_retweet.png"))

        # Positive_tweet = df[df['sentiment']=='Positive'].reset_index()
        # Negative_tweet = df[df['sentiment']=='Negative'].reset_index()
        # Neutral_tweet = df[df['sentiment']=='Neutral'].reset_index()

        # data_verified=df[(df['user_verified']==True)].reset_index()
        # data_not_verified=df[(df['user_verified']==False)].reset_index()

        # plt.figure(figsize=(8, 8))
        # sns.barplot(x="user_followers", y="user_name", orient="h", palette=["b"],
        #         data=df[(df.sentiment== "Positive")]\
        #         .drop_duplicates(subset=["user_name"])\
        #         .sort_values(by=["user_followers"], ascending=False)[["user_name", "user_followers"]][:10])
        # plt.title('Top 10 Accounts with Highest Followers who tweet Positive')
        # #31
        # plt.savefig(os.path.join(self.bar_dir, "31top positive.png"))

        # plt.figure(figsize=(8, 8))
        # sns.barplot(x="user_followers", y="user_name", orient="h", palette=["g"],
        #         data=df[(df.sentiment == "Neutral")]
        #         .drop_duplicates(subset=["user_name"])\
        #         .sort_values(by=["user_followers"], ascending=False)[["user_name", "user_followers"]][:10])
        # #32
        # plt.title('Top 10 Accounts with Highest Followers who tweet Neutral')
        # plt.savefig(os.path.join(self.bar_dir, "32top neutral.png"))

        # plt.figure(figsize=(8, 8))
        # sns.barplot(x="user_followers", y="user_name", orient="h", palette=["r"],
        #         data=df[(df.sentiment == "Negative")]
        #         .drop_duplicates(subset=["user_name"])\
        #         .sort_values(by=["user_followers"], ascending=False)[["user_name", "user_followers"]][:10])
        # plt.title('Top 10 Accounts with Highest Followers who tweet Negative')
        # #33
        # plt.savefig(os.path.join(self.bar_dir, "33top negative.png"))

class Pie:
    def __init__(self):
        self.pie_dir = "figures/pie"
        Path(self.pie_dir).mkdir(parents=True, exist_ok=True)

    def plot_pie(self, data, title):
        plt.figure(figsize=(8,8))
        # data.plot(kind = 'pie', title = title)
        # plt.savefig(os.path.join(self.pie_dir, title + ".png"))
        return

    def verified_pie(self):
        df = pd.read_csv("data/vaccination_tweets.csv")
        verified = df[df["user_verified"]==True].shape[0]
        non_verified = df[df["user_verified"]==False].shape[0]
        
        labels = ['not_verified', 'verified']
        sizes = [non_verified, verified]

        # plt.figure(figsize=(8,8))
        # plt.pie(x=sizes, labels=labels)
        # plt.savefig(os.path.join(self.pie_dir,  "verified_pie.png"))

        return (labels, sizes)

    def coutry_pie(self, df, k, col_name, country):
        pla = df[col_name][df['user_location'] == country].value_counts().sort_values(ascending=False)
        title = 'Top ' + col_name + ' in' + country 
        
        self.plot_pie(pla[:k], title)

    def top_pie(self, k, col_name):
        df=pd.read_csv('data/vaccination_tweets.csv')
        top_tags=df[col_name].value_counts().sort_values(ascending=False)
        title = 'Top ' + str(k) + ' ' + col_name

        # self.plot_pie(top_tags[:k], title)
        return (list(top_tags[:k].index) , list(top_tags[:k].values))

    def sentiment_pie(self, df):
        neutral_thresh = 0.05

        # Obtain polarity scores generated by TextBlob
        df['score'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)

        # Convert polarity score into sentiment categories
        df['sentiment'] = df['score'].apply(lambda c: 'Positive' if c >= neutral_thresh else ('Negative' if c <= -(neutral_thresh) else 'Neutral'))

        positive = df[df['sentiment'].str.contains("Positive")].shape[0]
        neutral  = df[df['sentiment'].str.contains("Neutral")].shape[0]
        negative = df[df['sentiment'].str.contains("Negative")].shape[0]

        labels = 'positive', 'neutral', 'negative'
        sizes = [positive, neutral, negative]

        # plt.figure(figsize=(8,8))
        # plt.pie(x=sizes, labels=labels)
        # plt.savefig(os.path.join(self.pie_dir, "sentimental.png"))

class Wordcloud:
    def __init__(self):
        self.word_dir = "figures/word_cloud"
        Path(self.word_dir).mkdir(parents=True, exist_ok=True)

    def show_wordcloud(self, text, title):
        stop_words = set(STOPWORDS)
        stop_words.update(["t", "co", "https", "amp", "U"])
        wordcloud = WordCloud(stopwords=stop_words, scale=4, max_font_size=50, 
                max_words=500,background_color="black").generate(text)

        fig = plt.figure(1, figsize=(8,8))
        plt.axis('off')
        fig.suptitle(title)
        # plt.imshow(wordcloud, interpolation='bilinear')
        # plt.savefig(os.path.join(self.word_dir, title + ".png"))

    def text_wordcloud(self, df, col_name):
        data = df[col_name]
        title = 'Prevalent' + col_name + ' in tweets'     
        text = " ".join(t for t in data.dropna())

        self.show_wordcloud(text, title)

    # def country_wordcloud(self, df, col_name, country="United States"):
    #     us_df = df.loc[df.user_location==country]
    #     data = us_df[col_name]
    #     title = 'Prevalent' + col_name + 'in tweets from ' + country
    #     text = " ".join(t for t in data.dropna())

    #     self.show_wordcloud(text, title)

    def country_map(self, df):
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

        fig = px.choropleth(df_loc, locations = df_loc['index'],
                            color = df_loc['snd_loc'],locationmode='country names', hover_name = df_loc['snd_loc'], 
                            color_continuous_scale = px.colors.sequential.Inferno)
        fig.write_image(os.path.join(self.word_dir, "map.png"))  

class Line:
    def __init__(self):
        self.line_dir = "figures/line"
        Path(self.line_dir).mkdir(parents=True, exist_ok=True)

    def plot_line(self,x,y, data, title):
        
        fig = px.line(data, x=x, y=y, title=title)
        fig.write_image(os.path.join( self.line_dir, title + ".png"))
        
        return

    def month_engagement(self):
        df = pd.read_csv("data/vaccination_tweets.csv")
        df['date']=pd.to_datetime(df['date'])
        df['total_engagement']=df['retweets']+df['favorites']

        df = df.sort_values(by='date')
        df['date'] = df['date'].dt.strftime('%m/%y')       
        day_month = df.groupby('date', sort=False, as_index=False).agg({'total_engagement':'sum'})

        x='day'
        y='total_engagement'

        # self.plot_line(x, y, day_month, title)
        return (list(day_month['date'].values), list(day_month['total_engagement'].values))     

    def tweet_day_year(self, df):
        L = ['year', 'month', 'day', 'dayofweek', 'dayofyear', 'weekofyear', 'quarter']

        df['datedt'] = pd.to_datetime(df['date'])
        df['year'] = df['datedt'].dt.year
        df['month'] = df['datedt'].dt.month
        df['day'] = df['datedt'].dt.day
        df['dayofweek'] = df['datedt'].dt.dayofweek
        df['hour'] = df['datedt'].dt.hour
        df['minute'] = df['datedt'].dt.minute
        df['dayofyear'] = df['datedt'].dt.dayofyear
        df['date_only'] = df['datedt'].dt.date
        
        tweets_agg_df = df.groupby(["date_only"])["text"].count().reset_index()
        tweets_agg_df.columns = ["date_only", "count"]
        
        x='date_only'
        y='count'
        title="6Number of tweets per day of year"

        self.plot_line(x, y, tweets_agg_df, title)

    def sentiment_date(self, filename, sent):
        analyser = SentimentIntensityAnalyzer()

        df=pd.read_csv(filename)

        scores=[]
        sentiment=[]

        for i in range(len(df['text'])):
            score = analyser.polarity_scores(df['text'][i])
            score=score['compound']
            scores.append(score)

        for i in scores:
            if i>=0.05: sentiment.append('Positive')
            elif i<=(-0.05): sentiment.append('Negative')
            else: sentiment.append('Neutral')

        df['sentiment']=pd.Series(np.array(sentiment))
        df["date"] = pd.to_datetime(df.date) 

        timeline = df.resample('D', on='date')["sentiment"].value_counts().unstack(1)
        timeline.reset_index(inplace=True)
        timeline = timeline.melt("date", var_name='sentiment',  value_name='vals')

        x = "date"
        y = "vals"

        if sent == "positive":
            data = timeline[timeline['sentiment'].str.contains("Positive")]
            title = "pos_sentiment"
            self.plot_line(x, y, data, title)
        elif sent == "negative":
            data = timeline[timeline['sentiment'].str.contains("Negative")]
            title = "neg_sentiment"
            self.plot_line(x, y, data, title)
        elif sent == "neutral":
            data = timeline[timeline['sentiment'].str.contains("Neutral")]
            title = "neu_sentiment"     
            self.plot_line(x, y, data, title)       


