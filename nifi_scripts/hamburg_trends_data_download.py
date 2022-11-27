import sys
import pandas as pd
from pytrends.request import TrendReq
from datetime import datetime, timedelta


def get_interest_for_geo_and_term(geo, term, now):
    previous_date = now - timedelta(hours=24)
    pytrends = TrendReq(hl='en-US', tz=360)
    df_main = pytrends.get_historical_interest(
        [term], year_start=previous_date.year, month_start=previous_date.month, day_start=previous_date.day,
        hour_start=previous_date.hour, year_end=now.year, month_end=now.month, day_end=now.day, hour_end=now.hour,
        sleep=90, geo=geo)
    df_main = df_main.reset_index(drop=False)
    
    first_date = '-'.join([str(previous_date.year), str(previous_date.month), str(previous_date.day)])

    date_one = first_date + 'T' + str(previous_date.hour-1)
    date_two = first_date + 'T' + str(previous_date.hour+1)
    pytrends.build_payload([term], timeframe=date_one + ' ' + date_two)
    df_last_day = pytrends.interest_over_time().reset_index(drop=False)
    df_last_day['join_hour'] = [str(date.replace(microsecond=0, second=0, minute=0)) for date in df_last_day['date']]
    df_last_day.columns = ['date_exact', term, 'isPartial', 'date']
    df_last_day['date'] = df_last_day['date'].astype('datetime64[ns]')
    
    df_main = pd.merge(df_main, df_last_day, how="left", on=["date"])

    second_date = '-'.join([str(now.year), str(now.month), str(now.day)])

    date_three = second_date + 'T' + str(now.hour-1)
    date_four = second_date + 'T' + str(now.hour+2)

    pytrends.build_payload([term], timeframe=date_three + ' ' + date_four)
    df_first_day = pytrends.interest_over_time().reset_index(drop=False)
    df_first_day['join_hour'] = [str(date.replace(microsecond=0, second=0, minute=0)) for date in df_first_day['date']]
    df_first_day.columns = ['date_exact', term, 'isPartial', 'date']
    df_first_day['date'] = df_first_day['date'].astype('datetime64[ns]')

    df_main = pd.merge(df_main, df_first_day, how="left", on=["date"])
    
    df_main[term + '2'] = df_main[term] * (df_main[term + '_x']/100)
    df_main.loc[df_main[term + '2'].isna(),[term + '2']] = df_main[term + '_y'] * (df_main[term + '_x']/100)
    df_main.loc[df_main['date_exact_x'].isna(),['date_exact_x']] = df_main['date_exact_y']
    df_main = df_main.loc[~df_main['date_exact_x'].isna(),['date_exact_x', term + '2']].reset_index(drop=True)
    
    for i in range(df_main.shape[0]):
        element_date = df_main[['date_exact_x']].iloc[i][0]
        if type(element_date) == int:
            df_main.loc[i,['date_exact_x']] = datetime.utcfromtimestamp(int(element_date) / 1e9).strftime("%Y-%m-%d %H:%M:%S")
    df_main.columns = ['date', term]
    df_main['date'] = df_main['date'].astype(str)
    df_main['date'] = pd.to_datetime(df_main['date'], format='%Y-%m-%d %H:%M:%S')
    
    df_main2 = df_main.copy()
    df_main2['date'] = df_main2['date'] + timedelta(days=1)
    
    final = pd.merge(df_main[-5:], df_main2, how="left", on=["date"])
    final[term] = final[term + '_x'] - final[term + '_y']
    final = final[['date', term]]
    return final
    

def get_all_interest_for_geo(geo):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(['Facebook'], timeframe='now 1-H')
    df = pytrends.interest_over_time()
    now = datetime.strptime(str(df.index[-1]), "%Y-%m-%d %H:%M:%S")
    now
    output = get_interest_for_geo_and_term(geo=geo, term='Instagram', now = now)
    for topic in ['Twitter', 'YouTube', 'LinkedIn', 'Facebook']:
        out = get_interest_for_geo_and_term(geo=geo, term=topic, now = now)
        output = pd.merge(output, out, how="left", on=["date"])
    return output

geo = 'DE-HH'

df = get_all_interest_for_geo(geo=geo)
df.to_csv(sys.stdout, index=False)