import pandas as pd
import datetime as dt
import http.client
from io import StringIO
import time

def get_historic_20_days(conn, headers, location, start_date, end_date):
    request = "/history?startDateTime={}&aggregateHours=1&location={}&endDateTime={" \
              "}&unitGroup=metric&contentType=csv&shortColumnNames=false"
    request = request.format(start_date, location, end_date)

    conn.request("GET", request, headers=headers)

    res = conn.getresponse()
    data = res.read()

    s = str(data, 'utf-8')
    data_string = StringIO(s)
    df = pd.read_csv(data_string)

    return df


def get_historic_data(location, main_start_date, number_of_requests):
    conn = http.client.HTTPSConnection("visual-crossing-weather.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "c7b48b7c4emsh8a3b688e71b9896p1be4d0jsnda2e5b27b486",
        'X-RapidAPI-Host': "visual-crossing-weather.p.rapidapi.com"
    }

    start_dates_list = [main_start_date]

    for i in range(number_of_requests):
        start_dates_list.append(start_dates_list[i] + dt.timedelta(days=20))

    historic_dfs = dict()

    for i in range(number_of_requests):

        time.sleep(0.5)

        start_date = start_dates_list[i].strftime("%Y-%m-%dT%H:%M:%S")
        end_date = start_dates_list[i + 1].strftime("%Y-%m-%dT%H:%M:%S")

        try:
            df = get_historic_20_days(conn, headers, location, start_date, end_date)
            historic_dfs[start_date] = df

        except http.client.IncompleteRead:
            resp = "IncompleteRead ERROR DURING HISTORIC WEATHER DATA DOWNLOAD"
            historic_dfs[start_date] = resp
            print(start_date, resp)

        except http.client.CannotSendRequest:
            resp = "CannotSendRequest ERROR DURING HISTORIC WEATHER DATA DOWNLOAD"
            historic_dfs[start_date] = resp
            print(start_date, resp)
        except http.client.HTTPException:
            resp = "HTTPException ERROR DURING HISTORIC WEATHER DATA DOWNLOAD3"
            historic_dfs[start_date] = resp
            print(start_date, resp)
        except Exception:
            resp = "OTHER ERROR DURING HISTORIC WEATHER DATA DOWNLOAD"
            historic_dfs[start_date] = resp
            print(start_date, resp)

    return historic_dfs


