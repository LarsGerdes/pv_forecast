# pv_forecast
Here, a forecast for the energy production of a photovoltaic system is created.

## data
The data is collected from a Fronius Primo 5.0-1 inverter.
- pv.csv contains the original data.

## scripts
- pv_org.sql creates a database and uploads the original data.
- pv.ipynb shows an initial analysis and an explanation for the columns. 
- pv.sql creates a view without text columns and missing data.
- analysis.ipynb shows further analysis.
- sun_rise_set.ipynb download sunrise and sunset data.
