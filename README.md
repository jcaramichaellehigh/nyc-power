# nyc-power
Analysis of NYC grid load and weather

## Abstract
The goal of my project will be to model the relationship between weather/climate and power consumption in NYC. In addition to drawing on weather variables like temperature, humidity, and wind speed, I also include variables that model the economic rhythms of the city which drive also power consumption -- day of the week, holidays, etc. The response variable is the NYC grid load.

## Method
My model is a CatBoost model. CatBoost is an open-source library for gradient boosting on decision trees. It is similar to XGBoost or LightGBM. The final version of the model used  a tree depth of 10 and RMSE loss.

## Data
This projects uses two sources of data:

1. [NEX-GDDP-CMIP6](https://www.nccs.nasa.gov/services/data-collections/land-based-products/nex-gddp-cmip6) weather data and climate projections, downloaded from Google Earth Engine. This is daily data from 1950-2100 for several weather variables like temperature, humidity and wind speed.
   
2. [NYISO Load Data](https://www.nyiso.com/load-data), downloaded in one-year chunks. This is granular 5-minute tick data on grid load for the NYC region. 

## Instructions

- Download the NYISO data in one-year chunks via the website
- Download the NEX-GDDP-CMIP6 weather data from [GEE web API](https://www.code.earthengine.google.com), using the `google_earth_engine.js` script
- Modify any filepaths necessary to point the `.py` files to the downloaded data
- Run the `process_gddp.py` script
- Run the `process_load.py` script
- Run the `combine_data.py` script
- Run the `eda.py` script to generate plots
- Run the `catboost_model.py` to run the model and generate more plots

## Package requires
- `catboost`
- `matplotlib`
- `numpy`
- `os`
- `pandas`


