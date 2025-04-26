import pandas as pd
import os
import numpy as np
from pandas.tseries.holiday import USFederalHolidayCalendar

""" ============================================================================
    PEAK LOAD
============================================================================ """

load_dir = "/dmx/v-drive/Demex/Users/john.caramichael/scratch/school/dsci441/load"
df = pd.read_feather(load_dir + "/load.feather")

df_peak = df.groupby('date')['load'].max().reset_index()
df_peak = df_peak[df_peak['date'].dt.year <= 2024]

df_peak['log10_load'] = np.log10(df_peak['load'])

""" ============================================================================
    WX DATA
============================================================================ """

wx_dir = "/dmx/v-drive/Demex/Users/john.caramichael/scratch/school/dsci441/gddp"
wx =  pd.read_feather(wx_dir + "/gddp.feather")
df_peak = pd.merge(df_peak, wx, on='date', how='outer')
#%%

""" ============================================================================
    FINAL CLEAN + SAVE
============================================================================ """

# DOW
df_peak['dow'] = df_peak['date'].dt.day_of_week

df_peak['month'] = df_peak['date'].dt.month
# Holidays
cal = USFederalHolidayCalendar()
holidays = cal.holidays()
df_peak["holiday"] = (df_peak["date"].dt.date.isin(holidays.date))

# Business days
df_peak['bday'] = (df_peak['dow'] <= 4) & (df_peak['holiday'] == 0)

for var in ['dow', 'hurs', 'pr', 'rlds', 'rsds', 'sfcWind', 'tas', 'tasmax', 'tasmin']:
    df_peak[var + '_lag'] = df_peak[var].shift(1)
    df_peak[var + '_lag3'] = (df_peak[var].shift(1) + df_peak[var].shift(2) + df_peak[var].shift(3))/3

df_peak['covid'] = df_peak['date'].between("2020-03-16", "2021-06-15")

train_dir = "/dmx/v-drive/Demex/Users/john.caramichael/scratch/school/dsci441/training"
df_peak.to_feather(os.path.join(train_dir, "df_train.feather"))



