# Gets data from Fronius API and saves it in a PostgreSQL database on a
# RaspberryPi.

# Libraries
from toml import load           # loading config file
from requests import get        # API connection
from datetime import datetime   # timestamp operations
from psycopg2 import connect    # database connection

# Load data about IP and database access.
conf = load('conf.toml')

# URL to inverter
url = 'http://{}/solar_api/v1/GetInverterRealtimeData.cgi' \
      '?Scope=Device' \
      '&DeviceId=1' \
      '&DataCollection=CumulationInverterData'
url = url.format(conf['fronius']['ip'])

# Create API connection.
dic = get(url)
dic = dic.json()

# Convert local timezone aware string into UTC Unix Timestamp.
t = dic['Head']['Timestamp']
t = datetime.fromisoformat(t)
t = t.timestamp()
t = int(t)

# Connect to database.
conf = conf['database']
conn = connect(dbname=conf['name'],
               user=conf['user'],
               password=conf['password'],
               host=conf['host'],
               port=conf['port'])
cur = conn.cursor()

# Execute SQL statement.
try:
    cur.execute(
        'insert into energy_minute values (%s, %s)',
        (t, dic['Body']['Data']['TOTAL_ENERGY']['Value'])
    )
    conn.commit()
except KeyError:
    print(dic)

# Close database connection.
cur.close()
conn.close()
