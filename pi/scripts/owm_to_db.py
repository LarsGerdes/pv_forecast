# Requests weather forecasts from OWM API and saves it in PostgreSQL database
# on a Raspberry Pi.

from toml import load
from toml import dump

path = 'conf.toml'
conf = load(path)


if conf['owm_to_db']:

    # Libraries
    from requests import get
    from datetime import datetime
    from psycopg2 import connect
    from psycopg2.extras import execute_values

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

    conf['owm_to_db'] = False
    with open(path, 'w') as file:
        dump(conf, file)

else:
    conf['owm_to_db'] = True
    with open(path, 'w') as file:
        dump(conf, file)
