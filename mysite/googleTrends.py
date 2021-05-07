from pytrends.request import TrendReq
import pandas as pd
import time
startTime = time.time()
pytrend = TrendReq(hl='en-US', tz=360)

class Line:

    def google_line(self):
        colnames = ["keywords"]
        df = pd.read_csv("data/keyword_list.csv", names=colnames)
        df2 = df["keywords"].values.tolist()
        df2.remove("Keywords")

        dataset = []

        for x in range(0,len(df2)):
            keywords = [df2[x]]
            pytrend.build_payload(
            kw_list=keywords,
            cat=0,
            timeframe='2020-01-01 2021-05-01',
            geo='US')
            data = pytrend.interest_over_time()
            if not data.empty:
                data = data.drop(labels=['isPartial'],axis='columns')
                dataset.append(data)

        result = pd.concat(dataset, axis=1)
        result.to_csv('data/search_trends.csv')

        df3 = pd.read_csv("data/search_trends.csv")
        df3['date']=pd.to_datetime(df3.date)
        df3 = df3.sort_values(by='date')
        df3['date'] = df3['date'].dt.strftime('%m/%y')


        line = df3[['date', 'covid']]
        

        return list(line['date'].values), list(line['covid'].values)
        
class Bar:        

    def google_pfizer(self):
        colnames = ["keywords"]
        df = pd.read_csv("data/keyword_list2.csv", names=colnames)
        df2 = df["keywords"].values.tolist()
        df2.remove("Keywords")

        dataset = []

        for x in range(0,len(df2)):
            keywords = [df2[x]]
            pytrend.build_payload(
            kw_list=keywords,
            cat=0,
            timeframe='2021-01-01 2021-05-01',
            geo='US')
            data = pytrend.interest_over_time()
            if not data.empty:
                data = data.drop(labels=['isPartial'],axis='columns')
                dataset.append(data)

            result = pd.concat(dataset, axis=1)
            result.to_csv('data/search_trends2.csv')

        df3 = pd.read_csv("data/search_trends2.csv")
        df3['date']=pd.to_datetime(df3.date)
        df3 = df3.sort_values(by='date')
        df3['date'] = df3['date'].dt.strftime('%m/%y')


        line = df3[['date', 'pfizer']]
        

        return list(line['date'].values), list(line['pfizer'].values)
        
    def google_moderna(self):
        colnames = ["keywords"]
        df = pd.read_csv("data/keyword_list3.csv", names=colnames)
        df2 = df["keywords"].values.tolist()
        df2.remove("Keywords")

        dataset = []

        for x in range(0,len(df2)):
            keywords = [df2[x]]
            pytrend.build_payload(
            kw_list=keywords,
            cat=0,
            timeframe='2021-01-01 2021-05-01',
            geo='US')
            data = pytrend.interest_over_time()
            if not data.empty:
                data = data.drop(labels=['isPartial'],axis='columns')
                dataset.append(data)

            result = pd.concat(dataset, axis=1)
            result.to_csv('data/search_trends3.csv')

        df3 = pd.read_csv("data/search_trends3.csv")
        df3['date']=pd.to_datetime(df3.date)
        df3 = df3.sort_values(by='date')
        df3['date'] = df3['date'].dt.strftime('%m/%y')


        line = df3[['date', 'moderna']]
        

        return list(line['date'].values), list(line['moderna'].values)   

    def google_JJ(self):
        colnames = ["keywords"]
        df = pd.read_csv("data/keyword_list4.csv", names=colnames)
        df2 = df["keywords"].values.tolist()
        df2.remove("Keywords")

        dataset = []

        for x in range(0,len(df2)):
            keywords = [df2[x]]
            pytrend.build_payload(
            kw_list=keywords,
            cat=0,
            timeframe='2021-01-01 2021-05-01',
            geo='US')
            data = pytrend.interest_over_time()
            if not data.empty:
                data = data.drop(labels=['isPartial'],axis='columns')
                dataset.append(data)

            result = pd.concat(dataset, axis=1)
            result.to_csv('data/search_trends4.csv')

        df3 = pd.read_csv("data/search_trends4.csv")
        df3['date']=pd.to_datetime(df3.date)
        df3 = df3.sort_values(by='date')
        df3['date'] = df3['date'].dt.strftime('%m/%y')


        line = df3[['date', 'J&J Vaccine']]
        

        return list(line['date'].values), list(line['J&J Vaccine'].values)        