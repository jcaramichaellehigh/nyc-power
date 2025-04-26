import os
import pandas as pd

base_dir = "/dmx/v-drive/Demex/Users/john.caramichael/scratch/school/dsci441/gddp"

file = os.path.join(base_dir, 'GDDP_CMIP6_CNRM-ESM2-1.csv')
df = pd.read_csv(file)

# Unpack index
df[['scenario', 'model', 'date', 'i1', 'i2']] = df['system:index'].str.split(pat='_', expand=True)

# Keep only historical and SSP 8.5
df =df[df['scenario'].isin(['historical', 'ssp585'])]

# Format date
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
df['year'] = df['date'].dt.year

# Merge coordinate
df_coord = pd.DataFrame(
    {'name': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6'],
     'lat': [40.625, 40.625, 40.625, 40.875, 40.875, 40.875],
     'lon': [-74.125, -73.875, -73.625, -74.125, -73.875, -73.625]
     })

df = pd.merge(df, df_coord, on='name')
df = df[['model', 'year', 'date', 'hurs', 'lat', 'lon', 'pr', 'rlds', 'rsds', 'sfcWind', 'tas', 'tasmax', 'tasmin']]

df.to_feather(os.path.join(base_dir, "gddp.feather"))
