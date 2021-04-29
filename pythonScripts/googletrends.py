import pandas as pd
from pytrends.request import TrendReq
def google(string):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[string])

    dfTime = pytrend.interest_over_time()
    dfRegion = pytrend.interest_by_region()

    dfRegionSorted = pd.DataFrame(dfRegion, columns=['Covid19']).sort_values('Covid19', ascending=False)

    dfRegionSorted.to_csv("data/Sorted.csv")
    dfTime.to_csv("data/GoogleTrendsInterest.csv")
    # dfRegion.to_csv("GoogleTrendsRegion.csv")
    # dbTime = pd.DataFrame(columns=['date', 'interest'])
