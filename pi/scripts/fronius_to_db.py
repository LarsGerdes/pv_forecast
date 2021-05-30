# Accesses data from Fronius API and saves it in PostgreSQL database on a
# RaspberryPi.

# Libraries
from toml import load                       # loading config file
from requests import get                    # API connection
from psycopg2 import connect                # database connection

# Load data for IP and database access.
conf = load('conf.toml')

# URL to inverter
url = 'http://{}/solar_api/v1/GetInverterRealtimeData.cgi' \
      '?Scope=Device' \
      '&DeviceId=1' \
      '&DataCollection=CumulationInverterData'
url = url.format(conf['fronius'])

# Create API connection.
dic = get(url)
dic = dic.json()

# Select Timestamp and value of total energy
dt = dic['Head']['Timestamp']
wh = dic['Body']['Data'].get('TOTAL_ENERGY')

# Write data only to database if it is not None.
if wh is not None:

    wh = wh['Value']

    # Connect to database.
    conn = connect(**conf['database'])
    cur = conn.cursor()

    # Execute SQL statement.
    cur.execute('insert into energy_minute values (%s, %s)', (dt, wh))
    conn.commit()

    # Close database connection.
    cur.close()
    conn.close()
