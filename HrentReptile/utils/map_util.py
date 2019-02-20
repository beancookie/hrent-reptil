import requests
import re

def geocode(city, address):
    parameters = {'address': city + address, 'key': '8ea44dbee078819bc8ea60e65debad03'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    location = response.json()['geocodes'][0]['location']
    geo_point = {'lon': location.split(',')[0], 'lat': location.split(',')[1]}
    return geo_point


if __name__ == '__main__':
    print(geocode('南京', '中垠紫金观邸'))
