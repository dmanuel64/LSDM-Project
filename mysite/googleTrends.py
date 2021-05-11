from pytrends.request import TrendReq
import pandas as pd
import time
startTime = time.time()
pytrend = TrendReq(hl='en-US', tz=360)

class Line:

    def google_line(self, keywords):
        dataset = []

        pytrend.build_payload(kw_list=[keywords], cat=0, timeframe='2020-01-01 2021-05-01',geo='US')
        data = pytrend.interest_over_time()

        if not data.empty:
            data = data.drop(labels=['isPartial'],axis='columns')
            dataset.append(data)

        result = pd.concat(dataset, axis=1)
        result.reset_index(level=0, inplace=True)
        result['date']=pd.to_datetime(result.date)
        result = result.sort_values(by='date')
        result['date'] = result['date'].dt.strftime('%m/%y')

        line = result[['date', keywords]]
        
        return list(line['date'].values), list(line[keywords].values)
        
class Bar:        

    def google_bar(self, keywords):
        dataset = []

        pytrend.build_payload(kw_list=[keywords],cat=0,timeframe='2021-01-01 2021-05-01',geo='US')
        data = pytrend.interest_over_time()

        if not data.empty:
            data = data.drop(labels=['isPartial'],axis='columns')
            dataset.append(data)

        result = pd.concat(dataset, axis=1)
        result.reset_index(level=0, inplace=True)
        result['date']=pd.to_datetime(result.date)
        result = result.sort_values(by='date')
        result['date'] = result['date'].dt.strftime('%m/%y')

        line = result[['date', keywords]]
        
        return list(line['date'].values), list(line[keywords].values)
              