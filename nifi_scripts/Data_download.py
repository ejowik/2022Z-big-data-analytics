# def import_or_install(package):
#     try:
#         __import__(package)
#     except ImportError:
#         pip.main(["install", package])

import datetime
import sys
import time
import pandas as pd
import http.client
from io import StringIO

time.sleep(5)

locations = ["Berlin", "Hamburg","Bremen"]


conn = http.client.HTTPSConnection("visual-crossing-weather.p.rapidapi.com")

headers = {
    "X-RapidAPI-Key": "c7b48b7c4emsh8a3b688e71b9896p1be4d0jsnda2e5b27b486",
    "X-RapidAPI-Host": "visual-crossing-weather.p.rapidapi.com"
}

conn.request("GET", "/forecast?location=Hamburg&aggregateHours=1&shortColumnNames=0&unitGroup=metric&contentType=csv",
             headers=headers)

res = conn.getresponse()
data = res.read()

s = str(data, 'utf-8')
data_string = StringIO(s)
df = pd.read_csv(data_string)

df2 = df.copy()
df2.index = pd.to_datetime(df2["Date time"])
df2 = df2.asfreq(freq="1min")
df2 = df2.interpolate(method ='linear', limit_direction ='forward')
df2["Conditions"] = df2.Conditions.fillna(method="backfill")
df2["Address"] = df2.Address[0]
df2["Date time"] = df2.index
df2["Resolved Address"] = df2.Name[0]
df2["Name"] = df2.Name[0]

# we're taking 10 days of a forecast
# now = datetime.datetime.now()
# minutes = now.minute
# df3 = df2.iloc[minutes-1:60*24*10, :]
df3 = df2.iloc[:60*24*10, :]
df3.to_csv(sys.stdout, index=False)