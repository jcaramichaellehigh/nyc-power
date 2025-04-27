import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

base_dir = "data/load"
df = pd.read_feather(base_dir + "/load.feather")

""" =========================================================
GRID LOAD DAILY
========================================================= """

# Define percentiles
percentiles = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95]
agg_funcs = {'load': ['min'] + [lambda x, q=q: np.percentile(x, q) for q in percentiles] + ['max']}
result = df[['time', 'load']].groupby('time').agg(agg_funcs)
result.columns =  ['p0'] + [f'p{q}' for q in percentiles] + ['p100']
result = result.reset_index()

percentile_pairs = [(0, 100), (5, 95), (10, 90), (20, 80), (30, 70), (40, 60)]
shades = [plt.cm.gray_r(i) for i in np.linspace(0.2, 0.8, len(percentile_pairs))]

fig, ax = plt.subplots(figsize=(12, 6))
result['time'] = pd.to_datetime(result['time'], format='%H:%M:%S').apply(
    lambda t: pd.Timestamp('1900-01-01') + pd.to_timedelta(t.strftime('%H:%M:%S'))
)
for (p_low, p_high), shade in zip(percentile_pairs, shades):
    ax.fill_between(result['time'], result[f'p{p_low}'], result[f'p{p_high}'],
                    color=shade, label=f'{p_low}-{p_high}%')
ax.plot(result['time'], result['p50'], color='black', linewidth=2, label='Median')

ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.xticks(rotation=45)
ax.set_xlabel('Time')
ax.set_ylabel('Load')
ax.set_title('NYC Power Grid Load (2006-2024)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f} MW"))
ax.grid()
ax.legend()
plt.show()

""" =========================================================
PEAK
========================================================= """

df_peak = df.groupby('date')['load'].max().reset_index()
df_peak = df_peak[df_peak['date'].dt.year <= 2024]
df_peak['doy'] = df_peak['date'].apply(lambda x: pd.Timestamp(year=1904, month=x.month, day=x.day))
df_peak.set_index('doy', inplace=True)
df_peak_min = df_peak['load'].resample('W').min()
df_peak_max = df_peak['load'].resample('W').max()
df_peak_med = df_peak['load'].resample('W').median()

fig, ax = plt.subplots(figsize=(12, 6))
ax.fill_between(df_peak_min.index, df_peak_min, df_peak_max, color='lightgray', label='Weekly Range')
ax.plot(df_peak_med, color='black', linewidth=2, label='Weekly Median')
ax.set_title('NYC Peak Load (2006-2024)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f} MW"))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%B'))
ax.legend()
ax.grid()
plt.show()


""" =======================================================
PEAK VS. WX
======================================================= """
base_dir = "data/wx"

wx =  pd.read_feather(base_dir + "/gddp.feather")
df_peak = pd.merge(df_peak, wx, on='date', how='left')


fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter((df_peak['tasmax'] - 273.15) * 9/5 + 32, df_peak['load'], s=1.5, alpha=0.3, color='black')
ax.set_xlabel('Max Temperature (F)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f} MW"))
ax.set_title('NYC Peak Load (2006-2024) vs. Daily Max Temperature')
plt.show()


""" =======================================================
DISTRIBUTION
======================================================= """

xspace = np.linspace(4000, 12000)

fig, ax = plt.subplots(figsize=(7, 6))
ax.hist(df_peak['load'], bins=50, color='darkgray')

ax.set_title("NYC Peak Load")
ax.set_xlabel("Peak Load (MW)")

plt.show()


""" =======================================================
DISTRIBUTION
======================================================= """

import seaborn as sns
sns.kdeplot(df, x='load', hue='bday', fill=True,
            common_norm=False)
plt.title("NYC Peak Load (2006-2024) Business Day")
plt.show()
