#!/usr/bin/env python3

import sys
import os

from influxdb import InfluxDBClient
import requests


env = os.environ.get


DB_HOST = env('INFLUXDB_HOST', 'localhost')
DB_PORT = int(env('INFLUXDB_PORT', '8086'))
DB_USER = env('INFLUXDB_USER', 'root')
DB_PASS = env('INFLUXDB_PASS', 'root')
DB_NAME = env('INFLUXDB_DB', 'spaceapi')
STATUS_URL = env('STATUS_URL', 'https://status.crdmp.ch/')


def main():
    # Influx client
    client = InfluxDBClient(DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME)

    # Create database if necessary
    if DB_NAME not in (d['name'] for d in client.get_list_database()):
        client.create_database(DB_NAME)

    # Request status response
    resp = requests.get(STATUS_URL)
    resp.raise_for_status()

    # Parse data
    data = resp.json()

    # Build datapoints
    datapoints = []
    for sensor in data['sensors']['people_now_present']:
        value = sensor['value']
        del sensor['value']
        datapoints.append({
            'measurement': 'people_present',
            'tags': sensor,
            'fields': {'value': value},
        })
    for sensor in data['sensors']['temperature']:
        value = sensor['value']
        del sensor['value']
        datapoints.append({
            'measurement': 'temperature',
            'tags': sensor,
            'fields': {'value': value},
        })

    # Write datapoints
    if not client.write_points(datapoints):
        print('Error: Could not write datapoints!')
        sys.exit(1)


if __name__ == '__main__':
    main()
