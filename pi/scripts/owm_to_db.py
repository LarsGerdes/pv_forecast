# Requests weather forecasts from OWM API and saves it in PostgreSQL database
# on a Raspberry Pi and creates a cronjob to run fronius_to_db.py only while
# the sun is shining.

from toml import load
from toml import dump
from requests import get
from datetime import datetime

path = 'conf.toml'
conf = load(path)

# URL for OWM API
url = 'https://api.openweathermap.org/data/2.5/onecall' \
      '?lat={lat}' \
      '&lon={lng}' \
      '&exclude=minutely,daily,alerts' \
      '&units=metric' \
      '&APPID={key}'
url = url.format(**conf['owm'])

# Connection to API
owm = get(url)
owm = owm.json()

# Request data every second day
if conf['owm_to_db']:

    # Libraries
    from psycopg2 import connect
    from psycopg2.extras import execute_values

    wea = []
    for row in owm['hourly']:

        # UNIX to datetime
        row['dt'] = datetime.fromtimestamp(row['dt'])

        # delete useless data
        del row['weather']

        # transform rain from dict to float and replace missing values with
        # zero.
        row['rain'] = row.get('rain', {}).get('1h', 0)

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

    # change owm_to_db parameter in conf file to False to stop the request on
    # the next day
    conf['owm_to_db'] = False
    with open(path, 'w') as file:
        dump(conf, file)

else:
    # If owm_to_db parameter was false, it should changed again to true, so the
    # next data the request is executed again
    conf['owm_to_db'] = True
    with open(path, 'w') as file:
        dump(conf, file)

# Get sunrise and sunset data from API and save it in cronjob which executes
# fronius_to_db script.
keys = ['sunrise', 'sunset']
sun = [datetime.fromtimestamp(owm['current'][sun]).hour for sun in keys]

cron = '* {}-{} * * * pi cd /home/pi/pv && /home/pi/.local/bin/pipenv ' \
       'run python scripts/fronius_to_db.py\n'.format(*sun)
with open('/etc/cron.d/pv', 'w') as file:
    file.write(cron)
