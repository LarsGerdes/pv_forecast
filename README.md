# pv_forecast
Here, a forecast for the energy production of a photovoltaic system is created.

## data
- pv.csv contains the original data collected from a Fronius Primo 5.0-1 
  inverter.
- owm_2020_12_29.json weather data from openweathermap.org

## scripts
### sql
- pv_org.sql creates a database and uploads the original data.
- pv.sql creates a view without text columns and missing data.
- ws.sql creates a time series with 30 minutes frequency based on the energy 
  ('energy_positiv_ws').
- results.sql creates a table for saving forecasts. The table is initialized 
  with a seasonal naive model which creates a prediction based on the day 
  before.  

### jupyter  
- pv.ipynb shows an initial analysis and an explanation for the columns.
- analysis.ipynb shows further analysis.
- sun_rise_set.ipynb download sunrise and sunset data from sunrise-sunset.org.
- owm.ipynb download weather data from owm.
- results.ipynb creates error measures and plots to compare predictions.
