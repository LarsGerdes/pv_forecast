# Load data from Fronius Solar API archive and store in database.
# Earliest entry is from 2020-10-10.
# 5 minute frequency

# Libraries
from toml import load
from requests import get
from datetime import date
from datetime import datetime
from datetime import timedelta
from psycopg2 import connect
from psycopg2.extras import execute_values

# Load data for IP and database access.
conf = load('conf.toml')

# URL to inverter
url = 'http://{}/solar_api/v1/GetArchiveData.cgi' \
      '?Scope=Device' \
      '&DeviceClass=Inverter' \
      '&DeviceId=1' \
      '&StartDate={}' \
      '&EndDate={}' \
      '&Channel=EnergyReal_WAC_Sum_Produced'

# Earliest date with data
start = date(2020, 10, 10)
# At May 3 begins the storing of realtime data.
stop = date(2021, 5, 2)
# One request can get up to 16 dates.
step = 16

# Loop through dates
values = []
for t in range(start.toordinal(), stop.toordinal(), step):

    # Transform dates and hand over to API
    origin = datetime.fromordinal(t)
    start = origin.date()
    end = start + timedelta(15)
    if end > stop:
        end = stop

    url_t = url.format(conf['fronius'], start, end)

    # Create API connection.
    dic = get(url_t)
    dic = dic.json()
    dic = dic['Body']['Data']['inverter/1']['Data']
    dic = dic['EnergyReal_WAC_Sum_Produced']['Values']

    # Transform dict to list and unix timestamps to datetime
    origin = origin.timestamp()

    for i in dic.items():
        dt = int(i[0]) + origin
        dt = datetime.fromtimestamp(dt)
        values.append([dt, i[1]])

    print(start)

# Connect to database.
conn = connect(**conf['database'])
cur = conn.cursor()

# execute SQL statement
execute_values(cur, 'INSERT INTO energy_minute_5 VALUES %s', values)
conn.commit()

# close connection
cur.close()
conn.close()
