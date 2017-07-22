import math
import re


class WeightCalculator(object):

    def __init__(self):
        super(WeightCalculator, self).__init__()
        self._geocoder = self._initialize_geocoder()

    def calculate(self, a, b):
        try:
            a_lat, a_long = self._numify(a['LAT']), self._numify(a['LON'])
        except:
            a_lat, a_long = self._geocoder[a['countryCode']]

        try:
            b_lat, b_long = self._numify(b['LAT']), self._numify(b['LON'])
        except:
            b_lat, b_long = self._geocoder[b['countryCode']]

        world_distance = math.sqrt((a_lat - b_lat) ** 2 + (a_long - b_long) ** 2)

        time_distance = abs(self._numify(a['birthyear']) - self._numify(b['birthyear']))

        occupation_mult = 100.0 if a['occupation'] != b['occupation'] else 1.0
        industry_mult = 100.0 if a['industry'] != b['industry'] else 1.0
        domain_mult = 100.0 if a['domain'] != b['domain'] else 1.0

        distance = (occupation_mult * industry_mult * domain_mult * 1.0) * (world_distance + time_distance) / 1000
        return distance

    def _initialize_geocoder(self):
        geocoder = {}

        with open('country_codes.txt', 'rb') as f:
            f.readline()

            for line in f.readlines():
                country_code, lat, lon, country_name = line.split(' ', 3)
                lat = float(lat)
                lon = float(lon)

                geocoder[country_code.upper()] = (lat, lon)

        return geocoder

    def _numify(self, val):
        matcher = re.compile('\d*\.{0,1}\d*')
        return float(matcher.match(val).group())
