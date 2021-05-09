import pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plot

def google(string):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[string])

    Time = pytrend.interest_over_time()
    Region = pytrend.interest_by_region()
    Region.to_csv('data/GoogleTrendsRegion.csv')

    dfTime = pd.DataFrame(Time, columns=[string])
    dfRegion = pd.read_csv('data/GoogleTrendsRegion.csv', usecols=['geoName', string])

    timeGraph(dfTime, string)
    trends = RegionGraph(dfRegion, string)
    return trends


def timeGraph(Time, string):
    plot.figure(figsize=(720 / 96, 320 / 96), dpi=96)
    plot.plot(Time[string], label=string)
    plot.xlabel("Time (Yr)")
    plot.ylabel("Interest over time")
    plot.title("Lowest Interest = 0, Highest Interest = 100")
    plot.xticks(rotation='vertical')
    plot.legend()
    plot.tight_layout()
    plot.savefig('static/img/testLine.png', dpi=96)
    plot.clf()
    plot.close()

def RegionGraph(Region, string):
    plot.figure(figsize=(480/96, 320/96), dpi=96)
    Region = Region.sort_values(by=string, ascending=False)
    Region = Region.head(10)
    explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    plot.pie(Region[string], explode=explode, labels=Region['geoName'], autopct='%1.1f%%')
    plot.axis('equal')
    plot.savefig('static/img/testPie.png', dpi=96)
    plot.clf()
    plot.close()
    return Region.iloc[0,0]
