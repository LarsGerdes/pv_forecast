# Create a crontab to run the fronius_to_db.py script every minute while the
# sun is shining. Source of sunrise and sunset data is sunrise-sunset.org.

# Libraries
from requests import get        # API connection
from toml import load           # Load .toml files
from datetime import datetime   # timestamp operations

# Get coordinates.
conf = load('conf.toml')
conf = conf['owm']

# URL for sunrise-sunset API.
url = 'https://api.sunrise-sunset.org/json' \
      '?lat={}' \
      '&lng={}' \
      '&formatted=0'
url = url.format(conf['lat'], conf['lng'])

# Create API connection.
dic = get(url)
dic = dic.json()['results']

# Reduce timestamp to hour and get local timezone.
r = datetime.fromisoformat(dic['sunrise']).astimezone().hour
s = datetime.fromisoformat(dic['sunset']).astimezone().hour

# Create crontab.
cron = '* {}-{} * * * pi cd /home/pi/pv && /home/pi/.local/bin/pipenv ' \
       'run python scripts/fronius_to_db.py\n'.format(r, s)
with open('/etc/cron.d/pv', 'w') as file:
    file.write(cron)
