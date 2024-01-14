import requests
from pprint import pprint
from time import ctime

# An API key is required to access the Neo API. Get your API key from: https://api.nasa.gov/
api_key = 'your_api_key_here'

# URL for Neo API
start_date = '2020-06-06'
end_date = '2020-06-07'
url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}'

# Making a request and getting data
r = requests.get(url)
data = r.json()

# Extracting asteroid data
neo = data['near_earth_objects']
for near in neo[start_date]:
    print(near['id'], near['name'], near['absolute_magnitude_h'])

# Asteroids by index in the list
first = neo[start_date][0]
print(first)

# Finding info by name
all_asteroids = neo[start_date]
for asteroid in all_asteroids:
    if asteroid['name'] == '163348 (2002 NN4)':
        pprint(asteroid)
        break

# Asteroid name
print(asteroid['name'])

# Asteroid ID
print(asteroid['id'])

# NASA URL
print(asteroid['nasa_jpl_url'])

# Absolute magnitude: luminosity
print(asteroid['absolute_magnitude_h'])

# Diameter
dia = asteroid['estimated_diameter']
print(dia)

# Average diameter
avg_dia_m = (dia['meters']['estimated_diameter_min'] + dia['meters']['estimated_diameter_max']) / 2
print(avg_dia_m)

# Is potentially hazardous
print(asteroid['is_potentially_hazardous_asteroid'])

# Close approach date
close_data = asteroid['close_approach_data']
pprint(close_data)

date = close_data[0]['epoch_date_close_approach']
print(ctime(date))

# Miss distance
miss_distance = close_data[0]['miss_distance']
print(miss_distance)

# Relative velocity
rel_vel = close_data[0]['relative_velocity']
print(rel_vel)

# Is Sentry object
print(asteroid['is_sentry_object'])
