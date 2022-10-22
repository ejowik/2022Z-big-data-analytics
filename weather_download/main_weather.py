import pandas
import pandas as pd
import pickle
from historical_weather_download import get_historic_data

# Settings
location = "Bremen"
initial_date = "2020-09-30T00:00:00"
initial_date_dt = pd.to_datetime(initial_date)

# Run requests and gather historical data, 37 x 20 days starting 2020-09-30
historic_dfs = get_historic_data(location, initial_date_dt, 37)

df_merged = pd.DataFrame(columns=historic_dfs[initial_date].columns)
for value in historic_dfs.values():
    df_merged = pd.concat([df_merged, value], axis=0)

df_merged = df_merged.reset_index(drop=True)
df_merged.to_csv("./merged_historic_{}.csv".format(location))
