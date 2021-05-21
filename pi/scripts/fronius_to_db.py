# Gets data from Fronius API and save it in PostgreSQL database on a
# RaspberryPi.

# Libraries
from toml import load                       # loading config file
from requests import get                    # API connection
from datetime import datetime, timezone     # timestamp operations
from psycopg2 import connect                # database connection

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

# Convert string to UTC datetime.
dt = dic['Head']['Timestamp']
dt = datetime.fromisoformat(dt)
dt = dt.astimezone(timezone.utc)

try:
    wh = dic['Body']['Data']['TOTAL_ENERGY']['Value']

    # Connect to database.
    conf = conf['database']
    conn = connect(dbname=conf['name'],
                   user=conf['user'],
                   password=conf['password'],
                   host=conf['host'],
                   port=conf['port'])
    cur = conn.cursor()

    # Execute SQL statement.
    cur.execute('insert into energy_minute values (%s, %s)', (dt, wh))
    conn.commit()

    # Close database connection.
    cur.close()
    conn.close()

except KeyError:
    # Sometimes the API is not accessible. However, this does not happen very
    # often. Therefore, the error message is simply suppressed.
    pass

