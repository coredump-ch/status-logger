#!/usr/bin/env python3

from influxdb import InfluxDBClient

DB_USER = 'root'
DB_PASS = 'root'
DB_NAME = 'spaceapi'

client = InfluxDBClient('localhost', 8086, DB_USER, DB_PASS, DB_NAME)

# Create database if necessary
if DB_NAME not in (d['name'] for d in client.get_list_database()):
    client.create_database(DB_NAME)

# Write a random datapoint
client.write_points([{
    'measurement': 'people_now_present',
    'fields': {
        'value': 42,
    },
}])
