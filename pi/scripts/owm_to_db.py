# Requests weather forecasts from OWM API and saves it in PostgreSQL database
# on a Raspberry Pi.

# Libraries
from toml import load
from requests import get
from datetime import datetime
from psycopg2 import connect
from psycopg2.extras import execute_values

# Load data for API access.
conf = load('conf.toml')

# URL for OWM API
url = 'https://api.openweathermap.org/data/2.5/onecall' \
      '?lat={lat}' \
      '&lon={lng}' \
      '&exclude=current,minutely,daily,alerts' \
      '&units=metric' \
      '&APPID={key}'
url = url.format(**conf['owm'])

# Connection to API
owm = get(url)
owm = owm.json()
owm = owm['hourly']
wea = []

for row in owm:

    # UNIX to datetime
    row['dt'] = datetime.fromtimestamp(row['dt'])

    # delete useless data
    del row['weather']

    # transform rain from dict to float and replace missing values with zero.
    if 'rain' in row:
        row['rain'] = next(iter(row['rain'].values()))
    else:
        row['rain'] = 0

    # dict to list
    wea.append(list(row.values()))

# connect database
conn = connect(**conf['database'])
cur = conn.cursor()

# execute SQL statement
execute_values(cur, 'INSERT INTO weather VALUES %s', wea)
conn.commit()

# close connection
cur.close()
conn.close()
