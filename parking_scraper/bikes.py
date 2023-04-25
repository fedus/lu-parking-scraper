import os
import yaml
import requests
import json

from .config import config

with open(os.path.dirname(os.path.realpath(__file__)) + '/config.yml', 'r') as config_data:
  api = yaml.load(config_data, yaml.BaseLoader)['api']['bikes']

def get_luxembourg():
  req = requests.get(api['luxembourg'], params={'apiKey': config.get('VELOH_API_KEY', None)})

  if req.status_code != 200:
    raise Exception(f"Unexpected status code from Veloh API call: {raw.status_code}")

  raw = req.json()

  total = {
    'city': 'Luxembourg',
    'station_name': 'total',
    'bikes': 0,
    'stands': 0,
    'capacity': 0
  }

  bikes = []

  warnings = ""

  for raw_bike in raw:
    bike = {
      'station_number': raw_bike['number'],
      'city': 'Luxembourg',
      'station_name': raw_bike['name'],
      'status': raw_bike['status'],
      'connected': raw_bike['connected'],
      'bikes': raw_bike['totalStands']['availabilities']['bikes'],
      'stands': raw_bike['totalStands']['availabilities']['stands'],
      'capacity': raw_bike['totalStands']['capacity']
    }

    if raw_bike['totalStands'] != raw_bike['mainStands']:
      warnings += f"{raw_bike['name']}: totalStands differs from mainStands\n"

    total['bikes'] += bike['bikes']
    total['stands'] += bike['stands']
    total['capacity'] += bike['capacity']

    bikes.append(bike)

  bikes.append(total)

  print(warnings)

  return bikes

def get_bikes():
  total = {
    'city': 'total',
    'station_name': 'total',
    'bikes': 0,
    'stands': 0,
    'capacity': 0
  }

  bikes = (get_luxembourg())

  for bike in bikes:
    if bike['station_name'] == 'total':
      total['bikes'] += bike['bikes']
      total['stands'] += bike['stands']
      total['capacity'] += bike['capacity']

  bikes.append(total)

  return bikes

if __name__ == '__main__':
  print(
    json.dumps(get_bikes())
  )
