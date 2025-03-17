# nyc-power
Analysis of NYC grid load and weather

## Abstract
The goal of my project will be to model the relationship between weather/climate and power consumption in NYC. In addition to drawing on weather variables like temperature, humidity, and wind speed from NEX-GDDP-CMIP6 developed by NASA, I will also include variables that model the economic rhythms of the city which drive also power consumption -- day of the week, holidays, etc. The response variable will be the NYC grid load, using granular data provided by NYISO (the grid operator) at the 5-minute increment. 

## Method
My baseline methodology is a GAM using a basic 80-20 train test split and no hyperparameter tuning. Future methdologies will consider more complex approaches like tree based models to handle complex feature interactions for weather variables

## Data
The data for this project is:
- [NEX-GDDP-CMIP6](https://www.nccs.nasa.gov/services/data-collections/land-based-products/nex-gddp-cmip6)
- [NYISO Load Data](https://www.nyiso.com/load-data)
