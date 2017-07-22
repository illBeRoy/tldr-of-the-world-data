import math
import re


class WeightCalculator(object):
    '''
    Distance based calculator.

    Gives precedence to occupation: people that have the same occupation and interests are most likely to appear first.
    Then takes into account the geographic distance between the two records, and the time distance as well.

    Uses an offline country geocoding dataset that's used as a fallback, in case a given record does not have
    lat\long values specified.
    '''

    def __init__(self):
        super(WeightCalculator, self).__init__()
        self._geocoder = self._initialize_geocoder()

    def calculate(self, a, b):

        # get lat\long values for a, use the geocoder as a fallback
        try:
            a_lat, a_long = self._numify(a['LAT']), self._numify(a['LON'])
        except:
            a_lat, a_long = self._geocoder[a['countryCode']]

        # get lat\long values for b, use the geocoder as a fallback
        try:
            b_lat, b_long = self._numify(b['LAT']), self._numify(b['LON'])
        except:
            b_lat, b_long = self._geocoder[b['countryCode']]

        # calculate geographic distance
        geographic_distance = math.sqrt((a_lat - b_lat) ** 2 + (a_long - b_long) ** 2)

        # calculate time distance
        time_distance = abs(self._numify(a['birthyear']) - self._numify(b['birthyear']))

        # create multiplier punishments for mismatching occupations, industries and domains
        occupation_mult = 100.0 if a['occupation'] != b['occupation'] else 1.0
        industry_mult = 100.0 if a['industry'] != b['industry'] else 1.0
        domain_mult = 100.0 if a['domain'] != b['domain'] else 1.0

        # calculate weight as distance
        distance = (occupation_mult * industry_mult * domain_mult * 1.0) * (geographic_distance + time_distance) / 1000

        # return calculated value
        return distance

    def _initialize_geocoder(self):
        '''
        Loads the country geocoding dataset into memory, to be used as fallback.

        :return: initialized geocoder
        '''
        geocoder = {}

        with open('country_geocoding.txt', 'rb') as f:
            f.readline()

            for line in f.readlines():
                country_code, lat, lon, country_name = line.split(' ', 3)
                lat = float(lat)
                lon = float(lon)

                geocoder[country_code.upper()] = (lat, lon)

        return geocoder

    def _numify(self, val):
        '''
        Extracts float value from string. More robust than the default "float" casting.

        :param val: value to convert to float
        :return: float value
        '''
        matcher = re.compile('\-{0,1}\d*\.{0,1}\d*')
        return float(matcher.match(val).group())
