import os
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar

cal = pd.tseries.holiday.USFederalHolidayCalendar()
holidays = cal.holidays()

base_dir = "/dmx/v-drive/Demex/Users/john.caramichael/scratch/school/dsci441/load"
file_names = os.listdir(base_dir)
file_names = [x for x in file_names if (".csv" in x)]

dfs = []
for file in file_names:

    file_dir = os.path.join(base_dir, file)
    print(file)
    df = pd.read_csv(file_dir)

    # Format ticks
    df['tick'] = pd.to_datetime(df['RTD End Time Stamp'])
    df.rename(columns={'RTD Actual Load': 'load'}, inplace=True)
    df = df[['tick', 'load']]

    # Dates
    df['date'] = df['tick'].dt.date
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['tick'].dt.year
    df['month'] = df['tick'].dt.month
    df['dow'] = df['tick'].dt.day_of_week
    df['time'] = df['tick'].dt.time
    df["holiday"] = (df["tick"].dt.date.isin(holidays.date))
    df['bday'] = (df['dow'] <= 5) & (df['holiday'] ==0)

    # Clean non-5min observations
    df = df[df['tick'].dt.second % 60 == 0]
    df = df[df.tick.dt.minute % 5 == 0]
    df = df[df['load'] > 0]

    dfs.append(df)

df = pd.concat(dfs, axis=0)
df.sort_values('tick', inplace=True)

df.to_feather(os.path.join(base_dir, "load.feather"))




